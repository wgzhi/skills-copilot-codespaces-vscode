using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;

namespace OPC2Modbus
{
    public class ConfigurationManager
    {
        private string configFilePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "config.json");

        public Configuration LoadConfiguration()
        {
            try
            {
                if (File.Exists(configFilePath))
                {
                    string json = File.ReadAllText(configFilePath);
                    return JsonConvert.DeserializeObject<Configuration>(json);
                }
                return null;
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error loading configuration: " + ex.Message);
                return null;
            }
        }

        public void SaveConfiguration(Configuration config)
        {
            try
            {
                string json = JsonConvert.SerializeObject(config, Formatting.Indented);
                File.WriteAllText(configFilePath, json);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error saving configuration: " + ex.Message);
            }
        }
    }

    public class Configuration
    {
        public string OPCServerName { get; set; }
        public string OPCServerIP { get; set; }
        public string ModbusMode { get; set; }
        public string SerialPort { get; set; }
        public int TCPPort { get; set; }
        public List<OPCTag> OPCTags { get; set; }

        public Configuration()
        {
            OPCTags = new List<OPCTag>();
            TCPPort = 502;
        }
    }
}