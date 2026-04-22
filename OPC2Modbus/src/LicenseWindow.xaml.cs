using System;
using System.Windows;

namespace OPC2Modbus
{
    public partial class LicenseWindow : Window
    {
        public LicenseWindow()
        {
            InitializeComponent();
            UpdateStatus();
        }

        private void UpdateStatus()
        {
            if (LicenseManager.IsLicenseValid())
            {
                txtStatus.Text = "Status: Licensed";
                txtStatus.Foreground = System.Windows.Media.Brushes.Green;
                btnRegister.Content = "Update License";
            }
            else
            {
                int remainingMinutes = LicenseManager.GetRemainingTrialMinutes();
                txtStatus.Text = string.Format("Status: Trial mode - {0} minutes remaining", remainingMinutes);
                txtStatus.Foreground = System.Windows.Media.Brushes.Orange;
                btnRegister.Content = "Register";
            }
        }

        private void btnRegister_Click(object sender, RoutedEventArgs e)
        {
            string licenseKey = txtLicenseKey.Text.Trim();
            if (string.IsNullOrEmpty(licenseKey))
            {
                MessageBox.Show("Please enter a license key", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            LicenseManager.RegisterLicense(licenseKey);
            if (LicenseManager.IsLicenseValid())
            {
                MessageBox.Show("License registered successfully", "Success", MessageBoxButton.OK, MessageBoxImage.Information);
                UpdateStatus();
            }
            else
            {
                MessageBox.Show("Invalid license key", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void btnCancel_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }
    }
}