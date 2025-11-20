@echo off
echo Starting Soil Health Monitoring System...
echo.
echo Make sure:
echo - Arduino is connected via USB
echo - Ollama is running (it starts automatically on Windows)
echo - COM port in app.py matches your Arduino
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5000
python app.py
