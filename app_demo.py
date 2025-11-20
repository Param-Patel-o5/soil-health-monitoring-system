from flask import Flask, render_template, request, jsonify
from llm_analyzer import SoilAnalyzer
import random
import time

# Import configuration
try:
    from config import USE_GEMINI, GEMINI_API_KEY
except ImportError:
    # Default values if config.py doesn't exist
    USE_GEMINI = True
    GEMINI_API_KEY = None

app = Flask(__name__)

# Demo mode - simulated sensor data
soil_analyzer = SoilAnalyzer(
    use_gemini=USE_GEMINI,
    gemini_api_key=GEMINI_API_KEY
)
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
    
    # Get LLM analysis
    print(f"\n🔍 Analyzing soil for: {farmer_input.get('crop')} in {farmer_input.get('location')}")
    print(f"   Using Gemini: {USE_GEMINI}")
    print(f"   API Key present: {bool(GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_API_KEY_HERE')}")
    
    recommendations = soil_analyzer.analyze_soil(current_data, farmer_input)
    
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
    print(f"   USE_GEMINI: {USE_GEMINI}")
    print(f"   GEMINI_API_KEY: {'Set' if GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_API_KEY_HERE' else 'NOT SET'}")
    print("\n" + "="*60 + "\n")
    app.run(debug=True, port=5000)
