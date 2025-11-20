# Configuration for Soil Health Monitoring System
# Copy this file to config.py and add your API key

# ============================================
# AI MODEL CONFIGURATION
# ============================================

# Use Google Gemini (RECOMMENDED - Fast & Free)
# Get your free API key from: https://aistudio.google.com/app/apikey
USE_GEMINI = True
GEMINI_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key

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
# Fallback Mode (if Gemini unavailable):
# - Rule-based analysis
# - Works instantly
# - No internet required
# - Basic but functional recommendations
