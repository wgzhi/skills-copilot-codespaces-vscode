# OPC2Modbus Test Guide

## Test Environment Setup

### Prerequisites
1. Windows operating system (XP/2000/2003/Win 7/Win8/Win Server 2003/Win Server 2008)
2. .NET Framework 4.6.2 or higher
3. An OPC server (e.g., Kepware KEPServerEX, MatrikonOPC Server, or any other OPC DA server)
4. A Modbus client (e.g., Modbus Poll, ModScan32, or any other Modbus client software)
5. Serial port (for Modbus RTU testing) or network connection (for Modbus TCP testing)

## Testing Steps

### 1. Basic Application Start
1. Run OPC2Modbus.exe
2. Verify that the application starts successfully
3. Check that the trial mode message appears if no license is present
4. Verify that the main window loads with all tabs and controls

### 2. OPC Server Connection
1. In the OPC Server tab:
   - Select an available OPC server from the dropdown list
   - Enter the OPC server IP address (localhost for local server)
   - Click "Connect" button
   - Verify that the connection is successful (status bar should show "Connected to OPC server")
   - Click "Browse Tags" button
   - Verify that the tag browser window opens and displays OPC tags
   - Select some tags and click "Select" to add them to the tag list

### 3. Modbus Server Configuration
1. In the Modbus Server tab:
   - Select Modbus RTU mode
   - Select a serial port from the dropdown list
   - Select an appropriate baud rate
   - OR select Modbus TCP mode and enter a TCP port (default: 502)
   - Click "Start Server" button
   - Verify that the server status changes to "Running"

### 4. Data Conversion Testing
1. Start your Modbus client software
2. For Modbus RTU:
   - Configure the client to use the same serial port and baud rate as OPC2Modbus
   - Set the slave ID to 1
3. For Modbus TCP:
   - Configure the client to connect to the IP address of the OPC2Modbus machine
   - Use the TCP port configured in OPC2Modbus
   - Set the unit ID to 1
4. Read holding registers from address 0
5. Verify that the values read from Modbus client match the values from the OPC server
6. Test with different data types (float, integer, boolean)

### 5. Configuration Management
1. Make changes to the configuration (e.g., add/remove tags, change Modbus settings)
2. Click "Save Configuration" from the File menu
3. Close and restart the application
4. Verify that the configuration is loaded correctly

### 6. Logging Testing
1. Perform various operations (connect/disconnect OPC server, start/stop Modbus server)
2. Check the Logs tab to verify that all operations are logged with timestamps
3. Close the application
4. Check the logs directory to verify that a log file is created with the current date

### 7. Licensing Testing
1. Run the application without a license key
2. Verify that the trial mode is active and countdown is working
3. Enter a valid license key (20 alphanumeric characters)
4. Verify that the application switches to licensed mode

### 8. Multi-language Testing
1. From the Language menu, select "Chinese"
2. Verify that the UI elements are displayed in Chinese
3. Switch back to "English" and verify the UI updates

## Troubleshooting

### Common Issues
1. **OPC server connection failed**: Ensure the OPC server is running and accessible
2. **Modbus server failed to start**: Check serial port permissions or TCP port availability
3. **No data in Modbus client**: Verify that OPC tags are enabled and OPC server is sending data
4. **License validation failed**: Ensure the license key is 20 alphanumeric characters

### Logs
Check the log files in the logs directory for detailed error messages and troubleshooting information.

## Test Results

| Test Case | Expected Result | Actual Result | Status |
|-----------|----------------|---------------|--------|
| Application Start | Application starts successfully | | |
| OPC Server Connection | Connection successful | | |
| Tag Browsing | Tags are displayed and selectable | | |
| Modbus Server Start | Server starts in RTU/TCP mode | | |
| Data Conversion | Modbus values match OPC values | | |
| Configuration Save/Load | Configuration persists after restart | | |
| Logging | Operations are logged with timestamps | | |
| Licensing | Trial mode and license validation work | | |
| Multi-language | UI switches between languages | | |
