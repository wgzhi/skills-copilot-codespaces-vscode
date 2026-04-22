using System;
using System.Windows;

namespace OPC2Modbus
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            
            // Check license
            if (!LicenseManager.IsLicenseValid())
            {
                if (LicenseManager.IsTrialExpired())
                {
                    MessageBox.Show("Trial period has expired. Please purchase a license.", "License Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    Current.Shutdown();
                    return;
                }
                
                MessageBox.Show("Running in trial mode. You have 30 minutes of usage.", "Trial Mode", MessageBoxButton.OK, MessageBoxImage.Information);
                LicenseManager.StartTrialTimer();
            }
        }
    }
}