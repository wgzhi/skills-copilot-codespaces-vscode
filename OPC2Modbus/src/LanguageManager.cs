using System;
using System.Collections.Generic;
using System.IO;
using System.Xml;

namespace OPC2Modbus
{
    public class LanguageManager
    {
        private Dictionary<string, string> translations;
        private string langDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "lang");

        public LanguageManager()
        {
            translations = new Dictionary<string, string>();
            if (!Directory.Exists(langDirectory))
            {
                Directory.CreateDirectory(langDirectory);
                // Create default language files
                CreateDefaultLanguageFiles();
            }
            // Default to English
            SetLanguage("en");
        }

        public void SetLanguage(string langCode)
        {
            translations.Clear();
            string langFilePath = Path.Combine(langDirectory, langCode + ".xml");
            if (File.Exists(langFilePath))
            {
                LoadLanguageFile(langFilePath);
            }
            else
            {
                // Fallback to English
                LoadLanguageFile(Path.Combine(langDirectory, "en.xml"));
            }
        }

        private void LoadLanguageFile(string filePath)
        {
            try
            {
                XmlDocument doc = new XmlDocument();
                doc.Load(filePath);
                XmlNode root = doc.SelectSingleNode("translations");
                if (root != null)
                {
                    foreach (XmlNode node in root.ChildNodes)
                    {
                        if (node.Name == "translation")
                        {
                            string key = node.Attributes["key"]?.Value;
                            string value = node.InnerText;
                            if (!string.IsNullOrEmpty(key))
                            {
                                translations[key] = value;
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error loading language file: " + ex.Message);
            }
        }

        public string GetTranslation(string key)
        {
            if (translations.ContainsKey(key))
            {
                return translations[key];
            }
            return key;
        }

        private void CreateDefaultLanguageFiles()
        {
            // Create English language file
            CreateLanguageFile("en.xml", new Dictionary<string, string>
            {
                { "OPCServer", "OPC Server" },
                { "ModbusServer", "Modbus Server" },
                { "Logs", "Logs" },
                { "Connect", "Connect" },
                { "Disconnect", "Disconnect" },
                { "BrowseTags", "Browse Tags" },
                { "StartServer", "Start Server" },
                { "StopServer", "Stop Server" },
                { "SaveConfiguration", "Save Configuration" },
                { "LoadConfiguration", "Load Configuration" },
                { "Exit", "Exit" },
                { "Language", "Language" },
                { "English", "English" },
                { "Chinese", "Chinese" },
                { "Help", "Help" },
                { "About", "About" },
                { "License", "License" },
                { "Server", "Server" },
                { "IPAddress", "IP Address" },
                { "Tags", "Tags" },
                { "TagName", "Tag Name" },
                { "ModbusAddress", "Modbus Address" },
                { "DataType", "Data Type" },
                { "Enable", "Enable" },
                { "Mode", "Mode" },
                { "SerialPort", "Serial Port" },
                { "BaudRate", "Baud Rate" },
                { "TCPPort", "TCP Port" },
                { "ServerStatus", "Server Status" },
                { "Ready", "Ready" },
                { "TrialMode", "Trial Mode" },
                { "Licensed", "Licensed" }
            });

            // Create Chinese language file
            CreateLanguageFile("zh.xml", new Dictionary<string, string>
            {
                { "OPCServer", "OPC服务器" },
                { "ModbusServer", "Modbus服务器" },
                { "Logs", "日志" },
                { "Connect", "连接" },
                { "Disconnect", "断开连接" },
                { "BrowseTags", "浏览标签" },
                { "StartServer", "启动服务器" },
                { "StopServer", "停止服务器" },
                { "SaveConfiguration", "保存配置" },
                { "LoadConfiguration", "加载配置" },
                { "Exit", "退出" },
                { "Language", "语言" },
                { "English", "英语" },
                { "Chinese", "中文" },
                { "Help", "帮助" },
                { "About", "关于" },
                { "License", "许可证" },
                { "Server", "服务器" },
                { "IPAddress", "IP地址" },
                { "Tags", "标签" },
                { "TagName", "标签名称" },
                { "ModbusAddress", "Modbus地址" },
                { "DataType", "数据类型" },
                { "Enable", "启用" },
                { "Mode", "模式" },
                { "SerialPort", "串口" },
                { "BaudRate", "波特率" },
                { "TCPPort", "TCP端口" },
                { "ServerStatus", "服务器状态" },
                { "Ready", "就绪" },
                { "TrialMode", "试用模式" },
                { "Licensed", "已授权" }
            });
        }

        private void CreateLanguageFile(string fileName, Dictionary<string, string> translations)
        {
            try
            {
                XmlDocument doc = new XmlDocument();
                XmlDeclaration declaration = doc.CreateXmlDeclaration("1.0", "utf-8", null);
                doc.AppendChild(declaration);
                XmlNode root = doc.CreateElement("translations");
                doc.AppendChild(root);
                foreach (var pair in translations)
                {
                    XmlNode translationNode = doc.CreateElement("translation");
                    XmlAttribute keyAttr = doc.CreateAttribute("key");
                    keyAttr.Value = pair.Key;
                    translationNode.Attributes.Append(keyAttr);
                    translationNode.InnerText = pair.Value;
                    root.AppendChild(translationNode);
                }
                doc.Save(Path.Combine(langDirectory, fileName));
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error creating language file: " + ex.Message);
            }
        }
    }
}