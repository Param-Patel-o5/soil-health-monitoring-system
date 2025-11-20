@echo off
echo ========================================
echo   DEMO MODE - No Arduino Required
echo ========================================
echo.
echo Testing the system with simulated sensors...
echo Opening browser in 3 seconds...
echo.
timeout /t 3 /nobreak >nul
start http://localhost:5000
python app_demo.py
