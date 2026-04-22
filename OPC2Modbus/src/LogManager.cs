using System;
using System.Collections.Generic;
using System.IO;

namespace OPC2Modbus
{
    public class LogManager
    {
        private List<string> logs;
        private string logDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs");

        public LogManager()
        {
            logs = new List<string>();
            if (!Directory.Exists(logDirectory))
            {
                Directory.CreateDirectory(logDirectory);
            }
        }

        public void AddLog(string logMessage)
        {
            logs.Add(logMessage);
        }

        public void SaveLog()
        {
            try
            {
                string logFilePath = Path.Combine(logDirectory, "OPC2Modbus_" + DateTime.Now.ToString("yyyy-MM-dd") + ".log");
                using (StreamWriter writer = new StreamWriter(logFilePath, true))
                {
                    foreach (string log in logs)
                    {
                        writer.WriteLine(log);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error saving log: " + ex.Message);
            }
        }
    }
}