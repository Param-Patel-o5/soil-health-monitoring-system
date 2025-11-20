from flask import Flask, render_template, request, jsonify
from sensor_reader import SensorReader
from llm_analyzer import SoilAnalyzer
import threading
import time

app = Flask(__name__)

# Global variables
sensor_reader = SensorReader(port='COM3')  # Change COM port as needed
soil_analyzer = SoilAnalyzer(model='llama3.2')
latest_sensor_data = {}
sensor_thread = None
reading_sensors = False

def read_sensors_continuously():
    """Background thread to continuously read sensor data"""
    global latest_sensor_data, reading_sensors
    
    if not sensor_reader.connect():
        print("Failed to connect to Arduino")
        return
    
    while reading_sensors:
        data = sensor_reader.read_sensor_data()
        if data:
            latest_sensor_data = data
        time.sleep(1)
    
    sensor_reader.close()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/sensor-data')
def get_sensor_data():
    """Get latest sensor readings"""
    return jsonify(latest_sensor_data)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze soil and provide recommendations"""
    farmer_input = request.json
    
    if not latest_sensor_data:
        return jsonify({'error': 'No sensor data available'}), 400
    
    # Get LLM analysis
    recommendations = soil_analyzer.analyze_soil(latest_sensor_data, farmer_input)
    
    return jsonify({
        'sensor_data': latest_sensor_data,
        'recommendations': recommendations
    })

@app.route('/api/start-sensors', methods=['POST'])
def start_sensors():
    """Start reading sensors"""
    global sensor_thread, reading_sensors
    
    if not reading_sensors:
        reading_sensors = True
        sensor_thread = threading.Thread(target=read_sensors_continuously, daemon=True)
        sensor_thread.start()
        return jsonify({'status': 'Sensors started'})
    
    return jsonify({'status': 'Sensors already running'})

@app.route('/api/stop-sensors', methods=['POST'])
def stop_sensors():
    """Stop reading sensors"""
    global reading_sensors
    reading_sensors = False
    return jsonify({'status': 'Sensors stopped'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
