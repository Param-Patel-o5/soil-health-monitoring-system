#include "DHT.h"
#include <SoftwareSerial.h>

// --- PIN DEFINITIONS ---
#define DHTPIN 2
#define DHTTYPE DHT11
#define MOISTURE_PIN A0

// RS485 Pins (Based on your success)
// Module RXD -> Arduino Pin 7 
// Module TXD -> Arduino Pin 4 
#define RX_PIN 7
#define TX_PIN 4

// MOISTURE SENSOR CALIBRATION
// CALIBRATED VALUES FOR YOUR SENSOR:
// Air (dry): 1023
// Water (wet): 650 (measured by immersing electrodes fully in water)
#define MOISTURE_AIR_VALUE 1023    // Sensor value in air (dry)
#define MOISTURE_WATER_VALUE 650   // Sensor value in water (wet) - CALIBRATED!

// Initialize Sensors
DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial rs485(RX_PIN, TX_PIN);

// NPK Command: Standard (Register 0x1E)
const uint8_t requestNPK[] = {0x01, 0x03, 0x00, 0x1E, 0x00, 0x03, 0x65, 0xCD};

// Variables to store sensor data
uint16_t valNitrogen, valPhosphorus, valPotassium;

void setup() {
  // Serial Monitor for PC (Keep at 9600 for viewing)
  Serial.begin(9600);
  
  // NPK Sensor Connection (MUST BE 4800 as found in test)
  rs485.begin(4800);
  
  dht.begin();
  
  Serial.println("Soil Monitor Ready");
  delay(1000);
}

bool readNPK() {
  valNitrogen = 0;
  valPhosphorus = 0;
  valPotassium = 0;
  
  // 1. Clear RS485 Buffer
  while (rs485.available()) rs485.read();
  
  // 2. Send Request
  rs485.write(requestNPK, sizeof(requestNPK));
  rs485.flush(); // Wait for data to leave Arduino
  
  // 3. Wait for Response (Timeout 1.5s)
  uint32_t start = millis();
  while (rs485.available() < 11) {
    if (millis() - start > 1500) {
      return false; // Timeout
    }
  }
  
  // 4. Read Data
  uint8_t buf[11];
  for (int i = 0; i < 11; i++) {
    buf[i] = rs485.read();
  }
  
  // 5. Check Header (Address 01, Function 03, Bytes 06)
  if (buf[0] == 0x01 && buf[1] == 0x03 && buf[2] == 0x06) {
    // Combine High Byte and Low Byte
    valNitrogen = (buf[3] << 8) | buf[4];
    valPhosphorus = (buf[5] << 8) | buf[6];
    valPotassium = (buf[7] << 8) | buf[8];
    return true;
  }
  
  return false;
}

void loop() {
  // --- 1. MOISTURE ---
  int moisture_raw = analogRead(MOISTURE_PIN);
  
  // Calculate moisture percentage (0-100%)
  // Formula: (air_value - current_value) / (air_value - water_value) * 100
  float moisture_percent = ((float)(MOISTURE_AIR_VALUE - moisture_raw) / (float)(MOISTURE_AIR_VALUE - MOISTURE_WATER_VALUE)) * 100.0;
  
  // Constrain to 0-100% range (in case of calibration errors)
  if (moisture_percent < 0) moisture_percent = 0;
  if (moisture_percent > 100) moisture_percent = 100;
  
  // --- 2. DHT (With Retry Logic) ---
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  // Retry once if failed (DHT sensors can be slow)
  if (isnan(h) || isnan(t)) {
    delay(200);
    h = dht.readHumidity();
    t = dht.readTemperature();
  }
  
  // --- 3. NPK ---
  int nitrogen = 0;
  int phosphorus = 0;
  int potassium = 0;
  
  if (readNPK()) {
    nitrogen = valNitrogen;
    phosphorus = valPhosphorus;
    potassium = valPotassium;
  }
  
  // --- OUTPUT JSON FOR PYTHON ---
  if (!isnan(h) && !isnan(t)) {
    Serial.print("{");
    Serial.print("\"temp\":");
    Serial.print(t, 1);  // 1 decimal place
    Serial.print(",\"humidity\":");
    Serial.print(h, 1);  // 1 decimal place
    Serial.print(",\"moisture\":");
    Serial.print(moisture_percent, 1);  // Now properly calibrated 0-100%
    Serial.print(",\"nitrogen\":");
    Serial.print(nitrogen);
    Serial.print(",\"phosphorus\":");
    Serial.print(phosphorus);
    Serial.print(",\"potassium\":");
    Serial.print(potassium);
    Serial.println("}");
  }
  
  delay(2000); // Read every 2 seconds
}
