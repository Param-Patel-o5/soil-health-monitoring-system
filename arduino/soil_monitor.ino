// Soil Health Monitoring System - Arduino Code

#include <DHT.h>

// Pin Definitions
#define DHTPIN 2
#define DHTTYPE DHT11
#define MOISTURE_PIN A0
#define NPK_RX 10
#define NPK_TX 11

DHT dht(DHTPIN, DHTTYPE);

// NPK Sensor variables (adjust based on your sensor model)
int nitrogen = 0;
int phosphorus = 0;
int potassium = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(MOISTURE_PIN, INPUT);
  
  Serial.println("Soil Monitor Ready");
}

void loop() {
  // Read Temperature & Humidity
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Read Soil Moisture (0-1023, convert to percentage)
  int moistureRaw = analogRead(MOISTURE_PIN);
  int moisture = map(moistureRaw, 0, 1023, 0, 100);
  
  // Read NPK values (implement based on your sensor)
  // This is a placeholder - adjust for your specific NPK sensor
  nitrogen = readNPKValue('N');
  phosphorus = readNPKValue('P');
  potassium = readNPKValue('K');
  
  // Send data in JSON-like format
  if (!isnan(temp) && !isnan(humidity)) {
    Serial.print("{");
    Serial.print("\"temp\":");
    Serial.print(temp);
    Serial.print(",\"humidity\":");
    Serial.print(humidity);
    Serial.print(",\"moisture\":");
    Serial.print(moisture);
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

// Placeholder function - implement based on your NPK sensor protocol
int readNPKValue(char nutrient) {
  // TODO: Implement actual NPK sensor reading
  // Different sensors use different protocols (RS485, I2C, etc.)
  return random(0, 100); // Placeholder random value
}
