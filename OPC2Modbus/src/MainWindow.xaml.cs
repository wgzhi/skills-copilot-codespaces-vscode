using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using OPCAutomation;
using NModbus4;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using Newtonsoft.Json;

namespace OPC2Modbus
{
    public partial class MainWindow : Window
    {
        private OPCServer opcServer;
        private OPCGroups opcGroups;
        private OPCGroup opcGroup;
        private List<OPCTag> opcTags;
        private IModbusSlave modbusSlave;
        private TcpListener tcpListener;
        private SerialPort serialPort;
        private Thread modbusServerThread;
        private bool isModbusServerRunning;
        private ConfigurationManager configManager;
        private LogManager logManager;
        private LanguageManager langManager;

        public MainWindow()
        {
            InitializeComponent();
            InitializeComponents();
            LoadConfiguration();
            UpdateLicenseStatus();
        }

        private void InitializeComponents()
        {
            opcTags = new List<OPCTag>();
            configManager = new ConfigurationManager();
            logManager = new LogManager();
            langManager = new LanguageManager();

            // Populate OPC servers
            PopulateOPCServers();
            // Populate serial ports
            PopulateSerialPorts();
            // Set default values
            cbModbusMode.SelectedIndex = 0;
            cbBaudRate.SelectedIndex = 0;
            txtServerStatus.Text = "Stopped";
            txtServerStatus.Foreground = Brushes.Red;
        }

        private void PopulateOPCServers()
        {
            try
            {
                opcServer = new OPCServer();
                object servers = opcServer.GetOPCServers(Environment.MachineName);
                foreach (var server in (Array)servers)
                {
                    cbOPCServer.Items.Add(server.ToString());
                }
                if (cbOPCServer.Items.Count > 0)
                {
                    cbOPCServer.SelectedIndex = 0;
                }
            }
            catch (Exception ex)
            {
                LogError("Failed to populate OPC servers: " + ex.Message);
            }
        }

        private void PopulateSerialPorts()
        {
            cbSerialPort.Items.Clear();
            foreach (var port in SerialPort.GetPortNames())
            {
                cbSerialPort.Items.Add(port);
            }
            if (cbSerialPort.Items.Count > 0)
            {
                cbSerialPort.SelectedIndex = 0;
            }
        }

        private void LoadConfiguration()
        {
            try
            {
                var config = configManager.LoadConfiguration();
                if (config != null)
                {
                    txtOPCIP.Text = config.OPCServerIP;
                    if (!string.IsNullOrEmpty(config.OPCServerName) && cbOPCServer.Items.Contains(config.OPCServerName))
                    {
                        cbOPCServer.SelectedItem = config.OPCServerName;
                    }
                    cbModbusMode.SelectedIndex = config.ModbusMode == "RTU" ? 0 : 1;
                    if (!string.IsNullOrEmpty(config.SerialPort) && cbSerialPort.Items.Contains(config.SerialPort))
                    {
                        cbSerialPort.SelectedItem = config.SerialPort;
                    }
                    txtTCPPort.Text = config.TCPPort.ToString();
                    opcTags = config.OPCTags;
                    dgOPCTags.ItemsSource = opcTags;
                }
            }
            catch (Exception ex)
            {
                LogError("Failed to load configuration: " + ex.Message);
            }
        }

        private void SaveConfiguration()
        {
            try
            {
                var config = new Configuration
                {
                    OPCServerName = cbOPCServer.SelectedItem?.ToString(),
                    OPCServerIP = txtOPCIP.Text,
                    ModbusMode = (cbModbusMode.SelectedItem as ComboBoxItem)?.Tag.ToString(),
                    SerialPort = cbSerialPort.SelectedItem?.ToString(),
                    TCPPort = int.Parse(txtTCPPort.Text),
                    OPCTags = opcTags
                };
                configManager.SaveConfiguration(config);
                LogInfo("Configuration saved successfully");
            }
            catch (Exception ex)
            {
                LogError("Failed to save configuration: " + ex.Message);
            }
        }

        private void ConnectOPC_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (opcServer == null)
                {
                    opcServer = new OPCServer();
                }
                string serverName = cbOPCServer.SelectedItem?.ToString();
                if (string.IsNullOrEmpty(serverName))
                {
                    MessageBox.Show("Please select an OPC server", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    return;
                }
                opcServer.Connect(serverName, txtOPCIP.Text);
                opcGroups = opcServer.OPCGroups;
                opcGroup = opcGroups.Add("Group1");
                opcGroup.UpdateRate = 1000;
                LogInfo("Connected to OPC server: " + serverName);
                txtStatus.Text = "Connected to OPC server";
            }
            catch (Exception ex)
            {
                LogError("Failed to connect to OPC server: " + ex.Message);
                txtStatus.Text = "Failed to connect to OPC server";
            }
        }

        private void DisconnectOPC_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (opcServer != null && opcServer.ServerState == (int)OPCServerState.OPCRunning)
                {
                    opcServer.Disconnect();
                    LogInfo("Disconnected from OPC server");
                    txtStatus.Text = "Disconnected from OPC server";
                }
            }
            catch (Exception ex)
            {
                LogError("Failed to disconnect from OPC server: " + ex.Message);
            }
        }

        private void BrowseTags_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (opcServer == null || opcServer.ServerState != (int)OPCServerState.OPCRunning)
                {
                    MessageBox.Show("Please connect to OPC server first", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    return;
                }
                var browser = new TagBrowser(opcServer);
                if (browser.ShowDialog() == true)
                {
                    var selectedTags = browser.SelectedTags;
                    foreach (var tag in selectedTags)
                    {
                        if (!opcTags.Any(t => t.TagName == tag))
                        {
                            opcTags.Add(new OPCTag { TagName = tag, ModbusAddress = "", DataType = "Float", Enable = true });
                        }
                    }
                    dgOPCTags.ItemsSource = null;
                    dgOPCTags.ItemsSource = opcTags;
                }
            }
            catch (Exception ex)
            {
                LogError("Failed to browse tags: " + ex.Message);
            }
        }

        private void StartModbusServer_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                string mode = (cbModbusMode.SelectedItem as ComboBoxItem)?.Tag.ToString();
                if (mode == "RTU")
                {
                    StartModbusRTUServer();
                }
                else
                {
                    StartModbusTCPServer();
                }
                isModbusServerRunning = true;
                modbusServerThread = new Thread(ModbusServerThread);
                modbusServerThread.Start();
                txtServerStatus.Text = "Running";
                txtServerStatus.Foreground = Brushes.Green;
                LogInfo("Modbus server started in " + mode + " mode");
            }
            catch (Exception ex)
            {
                LogError("Failed to start Modbus server: " + ex.Message);
            }
        }

        private void StartModbusRTUServer()
        {
            string portName = cbSerialPort.SelectedItem?.ToString();
            if (string.IsNullOrEmpty(portName))
            {
                throw new Exception("Please select a serial port");
            }
            int baudRate = int.Parse((cbBaudRate.SelectedItem as ComboBoxItem)?.Content.ToString());
            
            serialPort = new SerialPort(portName, baudRate, Parity.None, 8, StopBits.One);
            serialPort.Open();
            
            modbusSlave = ModbusSerialSlave.Create(1, serialPort);
            modbusSlave.DataStore = new DataStore();
        }

        private void StartModbusTCPServer()
        {
            int port = int.Parse(txtTCPPort.Text);
            tcpListener = new TcpListener(IPAddress.Any, port);
            tcpListener.Start();
            
            modbusSlave = ModbusTcpSlave.Create(1, tcpListener);
            modbusSlave.DataStore = new DataStore();
        }

        private void StopModbusServer_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                isModbusServerRunning = false;
                if (modbusServerThread != null && modbusServerThread.IsAlive)
                {
                    modbusServerThread.Join(2000);
                }
                if (modbusSlave != null)
                {
                    modbusSlave.Dispose();
                }
                if (tcpListener != null)
                {
                    tcpListener.Stop();
                }
                if (serialPort != null && serialPort.IsOpen)
                {
                    serialPort.Close();
                }
                txtServerStatus.Text = "Stopped";
                txtServerStatus.Foreground = Brushes.Red;
                LogInfo("Modbus server stopped");
            }
            catch (Exception ex)
            {
                LogError("Failed to stop Modbus server: " + ex.Message);
            }
        }

        private void ModbusServerThread()
        {
            try
            {
                modbusSlave.Listen();
                while (isModbusServerRunning)
                {
                    UpdateModbusData();
                    Thread.Sleep(1000);
                }
            }
            catch (Exception ex)
            {
                LogError("Modbus server error: " + ex.Message);
            }
        }

        private void UpdateModbusData()
        {
            try
            {
                if (opcServer == null || opcServer.ServerState != (int)OPCServerState.OPCRunning || opcGroup == null)
                {
                    return;
                }
                
                foreach (var tag in opcTags.Where(t => t.Enable))
                {
                    try
                    {
                        var item = opcGroup.OPCItems.AddItem(tag.TagName, 1);
                        Array values;
                        Array qualities;
                        Array times;
                        opcGroup.SyncRead(1, 1, new int[] { 1 }, out values, out qualities, out times);
                        
                        if (values != null && values.Length > 0)
                        {
                            // Update Modbus register based on data type
                            if (tag.DataType == "Float")
                            {
                                float value = Convert.ToSingle(values.GetValue(0));
                                // Convert float to two 16-bit registers
                                byte[] bytes = BitConverter.GetBytes(value);
                                ushort register1 = BitConverter.ToUInt16(bytes, 0);
                                ushort register2 = BitConverter.ToUInt16(bytes, 2);
                                // Update Modbus registers
                                modbusSlave.DataStore.HoldingRegisters[0] = register1;
                                modbusSlave.DataStore.HoldingRegisters[1] = register2;
                            }
                            else if (tag.DataType == "Integer")
                            {
                                int value = Convert.ToInt32(values.GetValue(0));
                                modbusSlave.DataStore.HoldingRegisters[0] = (ushort)value;
                            }
                            else if (tag.DataType == "Boolean")
                            {
                                bool value = Convert.ToBoolean(values.GetValue(0));
                                modbusSlave.DataStore.Coils[0] = value;
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        LogError("Error reading tag " + tag.TagName + ": " + ex.Message);
                    }
                }
            }
            catch (Exception ex)
            {
                LogError("Error updating Modbus data: " + ex.Message);
            }
        }

        private void SaveConfiguration_Click(object sender, RoutedEventArgs e)
        {
            SaveConfiguration();
        }

        private void LoadConfiguration_Click(object sender, RoutedEventArgs e)
        {
            LoadConfiguration();
        }

        private void Exit_Click(object sender, RoutedEventArgs e)
        {
            StopModbusServer_Click(sender, e);
            DisconnectOPC_Click(sender, e);
            logManager.SaveLog();
            Close();
        }

        private void SetLanguage_Click(object sender, RoutedEventArgs e)
        {
            string lang = (sender as MenuItem)?.Tag.ToString();
            if (!string.IsNullOrEmpty(lang))
            {
                langManager.SetLanguage(lang);
                // Refresh UI elements with new language
                LogInfo("Language changed to " + lang);
            }
        }

        private void About_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("OPC2Modbus v1.0.0\n\nProtocol converter from OPC to Modbus\n\nShanghai Xunrao Automation Technology Co., Ltd.", "About", MessageBoxButton.OK, MessageBoxImage.Information);
        }

        private void License_Click(object sender, RoutedEventArgs e)
        {
            var licenseWindow = new LicenseWindow();
            licenseWindow.ShowDialog();
        }

        private void LogInfo(string message)
        {
            string logMessage = "[INFO] " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") + " - " + message;
            txtLogs.AppendText(logMessage + "\n");
            txtLogs.ScrollToEnd();
            logManager.AddLog(logMessage);
        }

        private void LogError(string message)
        {
            string logMessage = "[ERROR] " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") + " - " + message;
            txtLogs.AppendText(logMessage + "\n");
            txtLogs.ScrollToEnd();
            logManager.AddLog(logMessage);
        }

        private void UpdateLicenseStatus()
        {
            if (LicenseManager.IsLicenseValid())
            {
                txtLicenseStatus.Text = "Licensed";
                txtLicenseStatus.Foreground = Brushes.Green;
            }
            else
            {
                txtLicenseStatus.Text = "Trial Mode";
                txtLicenseStatus.Foreground = Brushes.Orange;
            }
        }
    }

    public class OPCTag
    {
        public string TagName { get; set; }
        public string ModbusAddress { get; set; }
        public string DataType { get; set; }
        public bool Enable { get; set; }
    }
}