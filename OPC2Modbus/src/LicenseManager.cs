using System;
using System.IO;
using System.Threading;

namespace OPC2Modbus
{
    public static class LicenseManager
    {
        private static string licenseFilePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "license.dat");
        private static string trialFilePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "trial.dat");
        private static DateTime trialStartTime;
        private static Timer trialTimer;
        private static int remainingMinutes = 30;

        public static bool IsLicenseValid()
        {
            try
            {
                if (File.Exists(licenseFilePath))
                {
                    string licenseKey = File.ReadAllText(licenseFilePath).Trim();
                    // Simple license validation (in real application, use more secure method)
                    return licenseKey.Length == 20 && licenseKey.All(char.IsLetterOrDigit);
                }
                return false;
            }
            catch
            {
                return false;
            }
        }

        public static bool IsTrialExpired()
        {
            try
            {
                if (File.Exists(trialFilePath))
                {
                    string trialData = File.ReadAllText(trialFilePath);
                    if (DateTime.TryParse(trialData, out DateTime trialEndTime))
                    {
                        return DateTime.Now > trialEndTime;
                    }
                }
                // No trial file, start new trial
                return false;
            }
            catch
            {
                return true;
            }
        }

        public static void StartTrialTimer()
        {
            try
            {
                if (!File.Exists(trialFilePath))
                {
                    trialStartTime = DateTime.Now;
                    DateTime trialEndTime = trialStartTime.AddMinutes(30);
                    File.WriteAllText(trialFilePath, trialEndTime.ToString());
                }
                else
                {
                    string trialData = File.ReadAllText(trialFilePath);
                    if (DateTime.TryParse(trialData, out DateTime trialEndTime))
                    {
                        trialStartTime = DateTime.Now;
                        remainingMinutes = (int)(trialEndTime - trialStartTime).TotalMinutes;
                        if (remainingMinutes < 0)
                        {
                            remainingMinutes = 0;
                        }
                    }
                }

                // Start timer to check trial status
                trialTimer = new Timer(TrialTimerCallback, null, 0, 60000); // Check every minute
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error starting trial timer: " + ex.Message);
            }
        }

        private static void TrialTimerCallback(object state)
        {
            remainingMinutes--;
            if (remainingMinutes <= 0)
            {
                // Trial expired, shutdown application
                Console.WriteLine("Trial period expired");
                Environment.Exit(0);
            }
        }

        public static void RegisterLicense(string licenseKey)
        {
            try
            {
                File.WriteAllText(licenseFilePath, licenseKey);
                // Remove trial file if exists
                if (File.Exists(trialFilePath))
                {
                    File.Delete(trialFilePath);
                }
                // Stop trial timer if running
                if (trialTimer != null)
                {
                    trialTimer.Dispose();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error registering license: " + ex.Message);
            }
        }

        public static int GetRemainingTrialMinutes()
        {
            return remainingMinutes;
        }
    }
}