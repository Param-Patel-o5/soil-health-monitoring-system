@echo off
echo ========================================
echo   Soil Health Monitoring System
echo ========================================
echo.
echo Starting with Arduino (Real Sensors)...
echo.
echo Requirements:
echo - Arduino connected on COM4
echo - Sensors: DHT11, Moisture, NPK
echo - Internet (for AI analysis)
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5000
python app.py
