import serial
import json
import time

class SensorReader:
    def __init__(self, port='COM3', baudrate=9600):
        """Initialize serial connection to Arduino"""
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        
    def connect(self):
        """Connect to Arduino"""
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f"Connected to Arduino on {self.port}")
            return True
        except Exception as e:
            print(f"Error connecting to Arduino: {e}")
            return False
    
    def read_sensor_data(self):
        """Read and parse sensor data from Arduino"""
        if not self.serial_conn or not self.serial_conn.is_open:
            return None
            
        try:
            if self.serial_conn.in_waiting > 0:
                line = self.serial_conn.readline().decode('utf-8').strip()
                if line.startswith('{') and line.endswith('}'):
                    data = json.loads(line)
                    return data
        except Exception as e:
            print(f"Error reading sensor data: {e}")
        
        return None
    
    def close(self):
        """Close serial connection"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Serial connection closed")
