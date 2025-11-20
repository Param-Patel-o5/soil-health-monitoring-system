@echo off
echo ========================================
echo Soil Health Monitoring System - Setup
echo ========================================
echo.

echo Step 1: Installing Python packages...
pip install flask==3.0.0 pyserial==3.5 requests==2.31.0
echo.

echo Step 2: Checking if Ollama is installed...
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Ollama not found!
    echo Please download and install Ollama from: https://ollama.ai/download
    echo After installing, run: ollama pull llama3.2
    echo.
) else (
    echo Ollama found! Pulling llama3.2 model...
    ollama pull llama3.2
    echo.
)

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Upload arduino/soil_monitor.ino to your Arduino using Arduino IDE
echo 2. Check your Arduino's COM port in Device Manager
echo 3. Update the COM port in app.py (line 9)
echo 4. Run: python app.py
echo 5. Open browser: http://localhost:5000
echo.
pause
