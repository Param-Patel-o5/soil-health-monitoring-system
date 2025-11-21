from flask import Flask, render_template, request, jsonify
from llm_analyzer import SoilAnalyzer
from weather_service import WeatherService
import random
import time

# Import configuration
try:
    from config import USE_GEMINI, GEMINI_API_KEY, USE_WEATHER_API, OPENWEATHER_API_KEY
except ImportError:
    # Default values if config.py doesn't exist
    USE_GEMINI = True
    GEMINI_API_KEY = None
    USE_WEATHER_API = False
    OPENWEATHER_API_KEY = None

app = Flask(__name__)

# Demo mode - simulated sensor data
soil_analyzer = SoilAnalyzer(
    use_gemini=USE_GEMINI,
    gemini_api_key=GEMINI_API_KEY
)

# Weather service (optional enhancement)
weather_service = None
try:
    if USE_WEATHER_API and OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != "YOUR_OPENWEATHER_API_KEY":
        weather_service = WeatherService(OPENWEATHER_API_KEY)
        print("🌤️  Weather API: Enabled")
    else:
        print("🌤️  Weather API: Disabled (optional)")
except Exception as e:
    print(f"🌤️  Weather API: Failed to initialize ({e})")
    weather_service = None
demo_sensor_data = {
    'temp': 28.5,
    'humidity': 65,
    'moisture': 45,
    'nitrogen': 35,
    'phosphorus': 22,
    'potassium': 180
}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/sensor-data')
def get_sensor_data():
    """Get simulated sensor readings with slight variations"""
    simulated_data = {
        'temp': round(demo_sensor_data['temp'] + random.uniform(-2, 2), 1),
        'humidity': round(demo_sensor_data['humidity'] + random.uniform(-5, 5), 1),
        'moisture': round(demo_sensor_data['moisture'] + random.uniform(-3, 3), 1),
        'nitrogen': round(demo_sensor_data['nitrogen'] + random.uniform(-5, 5), 1),
        'phosphorus': round(demo_sensor_data['phosphorus'] + random.uniform(-3, 3), 1),
        'potassium': round(demo_sensor_data['potassium'] + random.uniform(-10, 10), 1)
    }
    return jsonify(simulated_data)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze soil and provide recommendations"""
    farmer_input = request.json
    
    # Use current simulated data
    current_data = {
        'temp': round(demo_sensor_data['temp'] + random.uniform(-1, 1), 1),
        'humidity': round(demo_sensor_data['humidity'] + random.uniform(-3, 3), 1),
        'moisture': round(demo_sensor_data['moisture'] + random.uniform(-2, 2), 1),
        'nitrogen': round(demo_sensor_data['nitrogen'] + random.uniform(-3, 3), 1),
        'phosphorus': round(demo_sensor_data['phosphorus'] + random.uniform(-2, 2), 1),
        'potassium': round(demo_sensor_data['potassium'] + random.uniform(-5, 5), 1)
    }
    
    # Get weather data if available (optional enhancement)
    weather_data = None
    if weather_service:
        try:
            location = farmer_input.get('location', '')
            print(f"🌤️  Fetching weather data for: {location}")
            weather_data = weather_service.get_weather_data(location)
            if weather_data:
                print(f"   ✓ Weather data retrieved successfully")
            else:
                print(f"   ✗ Weather data unavailable (continuing without it)")
        except Exception as e:
            print(f"   ✗ Weather API error: {e} (continuing without weather data)")
            weather_data = None
    
    # Get LLM analysis
    print(f"\n🔍 Analyzing soil for: {farmer_input.get('crop')} in {farmer_input.get('location')}")
    print(f"   Using Gemini: {USE_GEMINI}")
    print(f"   API Key present: {bool(GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_API_KEY_HERE')}")
    print(f"   Weather integration: {bool(weather_data)}")
    
    recommendations = soil_analyzer.analyze_soil(current_data, farmer_input, weather_data)
    
    print(f"✅ Analysis complete. Response length: {len(recommendations)} chars")
    
    return jsonify({
        'sensor_data': current_data,
        'recommendations': recommendations
    })

@app.route('/api/start-sensors', methods=['POST'])
def start_sensors():
    """Demo mode - sensors always available"""
    return jsonify({'status': '✅ Demo Mode: Simulated sensors started'})

@app.route('/api/stop-sensors', methods=['POST'])
def stop_sensors():
    """Demo mode - stop simulation"""
    return jsonify({'status': '⏸️ Demo Mode: Sensors paused'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌱 SOIL HEALTH MONITORING SYSTEM - DEMO MODE")
    print("="*60)
    print("\n📌 Running in DEMO mode with simulated sensor data")
    print("📌 No Arduino required for testing")
    print("📌 Open browser: http://localhost:5000")
    print(f"\n🔧 Configuration:")
    print(f"   AI Analysis (Gemini): {'Enabled' if USE_GEMINI and GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_API_KEY_HERE' else 'Disabled - Using Fallback'}")
    print(f"   Weather Enhancement: {'Enabled' if weather_service else 'Disabled (Optional)'}")
    print("\n" + "="*60 + "\n")
    app.run(debug=True, port=5000)
