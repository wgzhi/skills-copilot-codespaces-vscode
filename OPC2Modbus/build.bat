@echo off

rem Build script for OPC2Modbus application

setlocal

rem Set build parameters
set PROJECT_NAME=OPC2Modbus
set TARGET_FRAMEWORK=net462
set OUTPUT_DIR=bin\Release\%TARGET_FRAMEWORK%
set PACKAGE_DIR=OPC2Modbus_Portable

rem Create package directory if it doesn't exist
if not exist "%PACKAGE_DIR%" mkdir "%PACKAGE_DIR%"

rem Build the project
echo Building %PROJECT_NAME%...
dotnet build %PROJECT_NAME%.csproj -c Release -f %TARGET_FRAMEWORK%

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b %errorlevel%
)

rem Copy files to package directory
echo Copying files to package directory...
xcopy "%OUTPUT_DIR%\%PROJECT_NAME%.exe" "%PACKAGE_DIR%\" /Y
xcopy "%OUTPUT_DIR%\*.dll" "%PACKAGE_DIR%\" /Y
xcopy "%OUTPUT_DIR%\*.config" "%PACKAGE_DIR%\" /Y
xcopy "lang\" "%PACKAGE_DIR%\lang\" /E /Y

rem Create logs directory
if not exist "%PACKAGE_DIR%\logs" mkdir "%PACKAGE_DIR%\logs"

rem Create README file
echo Creating README file...
> "%PACKAGE_DIR%\README.txt" (
echo OPC2Modbus - Protocol Converter

echo ==============================

echo Description:

echo This software converts data from OPC server to Modbus server, supporting both Modbus RTU and TCP modes.

echo Usage:

echo 1. Run OPC2Modbus.exe

echo 2. Select OPC server and connect

echo 3. Browse and select OPC tags

echo 4. Configure Modbus server settings

echo 5. Start Modbus server

echo 6. Connect Modbus client to access data

echo Trial Mode:

echo - 30 minutes free trial without license

echo - After trial expires, you need to purchase a license

echo System Requirements:

echo - Windows XP/2000/2003/Win 7/Win8/Win Server 2003/Win Server 2008

echo - .NET Framework 4.6.2 or higher

echo - Serial port (for Modbus RTU) or network connection (for Modbus TCP)
)

echo Build and packaging completed successfully!
echo Package location: %CD%\%PACKAGE_DIR%

pause
