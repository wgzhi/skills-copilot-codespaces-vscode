# OPC2Modbus

## Description

OPC2Modbus is a protocol converter software that reads data from OPC servers and converts it to Modbus server format, supporting both Modbus RTU and Modbus TCP modes. This allows third-party devices or systems to access OPC server data through Modbus protocol.

## Features

- **Green software**: No installation required, ready to use after authorization
- **30-minute free trial**: Full functionality without license for 30 minutes
- **Multi-language support**: English and Chinese interfaces
- **OPC server connection**: Connect to local or remote OPC servers
- **Tag browsing**: Browse and select OPC tags for conversion
- **Modbus RTU mode**: Support for serial port communication
- **Modbus TCP mode**: Support for network communication
- **Configuration management**: Save and load configurations
- **Logging**: Auto-save time logs when program exits
- **License management**: Simple license registration process

## System Requirements

- Windows XP/2000/2003/Win 7/Win8/Win Server 2003/Win Server 2008
- .NET Framework 4.6.2 or higher
- Serial port (for Modbus RTU) or network connection (for Modbus TCP)
- OPC server (e.g., Kepware KEPServerEX, MatrikonOPC Server)

## Usage

1. Run OPC2Modbus.exe
2. Select OPC server from the dropdown list
3. Enter OPC server IP address (localhost for local server)
4. Click "Connect" to connect to OPC server
5. Click "Browse Tags" to select OPC tags
6. Configure Modbus server settings (mode, serial port/TCP port)
7. Click "Start Server" to start Modbus server
8. Connect Modbus client to access data

## Application Scenarios

### Scenario 1: Serial Port Access
Many production enterprises prohibit external TCP access to OPC servers for security reasons. OPC2Modbus can be deployed on the OPC server machine to convert OPC protocol to Modbus RTU protocol, allowing third-party hardware or systems to access data through serial ports.

### Scenario 2: Remote Access Solution
OPC2Modbus solves DCOM configuration issues encountered when accessing OPC servers remotely. By running OPC2Modbus on the OPC server machine, other computers can access the Modbus server instead of dealing with complex DCOM configurations.

### Scenario 3: Cross-Platform Integration
Linux-based devices (e.g., industrial touch screens) or devices without operating systems (e.g., PLCs) can access PC-based OPC servers through Modbus protocol, enabling system integration.

## Building and Packaging

To build and package the application:

1. Open the project in Visual Studio
2. Build the project in Release mode
3. Run the build.bat script to package the application as green software

The packaged application will be in the OPC2Modbus_Portable directory, ready for distribution without installation.

## License

This software is provided by Shanghai Xunrao Automation Technology Co., Ltd. For licensing information, please contact the company.
