# Configuration for Soil Health Monitoring System

# ============================================
# AI MODEL CONFIGURATION
# ============================================

# Option 1: Use Google Gemini (RECOMMENDED - Fast & Free)
# Get your free API key from: https://aistudio.google.com/app/apikey
USE_GEMINI = True
GEMINI_API_KEY = "AIzaSyB5EQ5pmt0ecNaI2vwyaY_Qmd-MjMjMV3k"  # Replace with your actual API key

# Weather API Configuration (OPTIONAL - Enhances accuracy but not required)
# Get free API key from: https://openweathermap.org/api
# System works perfectly fine without this
USE_WEATHER_API = False  # Set to True after getting valid API key from openweathermap.org
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"  # Replace with your key

# Note: This system uses Google Gemini exclusively for AI analysis
# Fallback mode provides rule-based analysis if Gemini is unavailable

# ============================================
# ARDUINO CONFIGURATION (for real hardware)
# ============================================
ARDUINO_COM_PORT = "COM3"  # Change to your Arduino's COM port
ARDUINO_BAUDRATE = 9600

# ============================================
# NOTES
# ============================================
# Google Gemini:
# - FREE (60 requests per minute)
# - Fast (3-10 seconds response)
# - High quality AI-powered analysis
# - Requires internet connection
# - Get API key: https://aistudio.google.com/app/apikey
#
# OpenWeatherMap API:
# - FREE (1000 calls per day)
# - Provides current weather + 5-day forecast
# - Improves AI accuracy with real-time climate data
# - Get API key: https://openweathermap.org/api
#
# Fallback Mode (if Gemini unavailable):
# - Rule-based analysis
# - Works instantly
# - No internet required
# - Basic but functional recommendations
