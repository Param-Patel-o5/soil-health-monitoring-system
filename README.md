# 🌱 Soil Health Monitoring System

AI-powered soil health monitoring system using Arduino sensors and Google Gemini AI. Provides real-time NPK analysis and intelligent, crop-specific fertilizer recommendations for farmers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Arduino](https://img.shields.io/badge/Arduino-Compatible-teal.svg)
![AI](https://img.shields.io/badge/AI-Google%20Gemini%202.5%20Flash-orange.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)

## 📋 Overview

This IoT-based agricultural solution combines Arduino sensors with Google Gemini AI to help farmers make data-driven decisions about soil health and crop management. The system reads real-time soil parameters (NPK, moisture, temperature, humidity) and provides intelligent, crop-specific recommendations in simple, farmer-friendly language.

### ✨ Key Features

- 🔬 **Real-time Monitoring**: 6 soil parameters (NPK, Temperature, Humidity, Moisture) updated every 2 seconds
- 🤖 **AI-Powered Analysis**: Google Gemini 2.5 Flash provides intelligent, context-aware recommendations
- 🌾 **Crop-Specific Advice**: Tailored recommendations for any crop, location, and season
- 💊 **Fertilizer Recommendations**: Exact quantities (kg/acre) with precise application timing
- 💧 **Smart Irrigation**: Moisture-based irrigation schedules with critical stage alerts
- 📅 **Seasonal Intelligence**: Kharif/Rabi/Zaid season suitability analysis
- 🌐 **Modern Web Interface**: Clean, responsive UI accessible from any device
- 🎯 **Demo Mode**: Full functionality without hardware for testing/presentations
- 🔄 **Fallback Mode**: Rule-based analysis when AI is unavailable
- ⚡ **Fast Response**: AI analysis in 3-10 seconds

## 🔧 Hardware Components

| Component | Model | Purpose | Pin |
|-----------|-------|---------|-----|
| Arduino | Uno/Nano/Mega | Main controller | - |
| NPK Sensor | RS485 | Nitrogen, Phosphorus, Potassium | RX:7, TX:4 |
| DHT11/DHT22 | Temperature & Humidity | Air conditions | Pin 2 |
| Soil Moisture | Analog | Soil water content | A0 |
| USB Cable | Data cable | Serial communication | - |

### Sensor Specifications

- **NPK Sensor**: RS485 protocol, 4800 baud, 0-2000 mg/kg range (Nitrogen, Phosphorus, Potassium)
- **DHT11**: Temperature 0-50°C (±2°C accuracy), Humidity 20-90% (±5% accuracy)
- **Soil Moisture**: Analog sensor 0-1023 (converted to 0-100% in code)

## 💻 Software Requirements

- Python 3.8 or higher
- Arduino IDE
- Google Gemini API Key (free)
- Internet connection

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Param-Patel-o5/soil-health-monitoring-system.git
cd soil-health-monitoring-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

1. Get free API key: [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Open `config.py`
3. Replace the placeholder with your key:
```python
USE_GEMINI = True
GEMINI_API_KEY = "your-api-key-here"
```

**Note**: The system works without API key in fallback mode, but AI recommendations are much better!

### 4. Upload Arduino Code

1. Open Arduino IDE
2. Install required libraries: `DHT sensor library` (by Adafruit)
3. File → Open → `arduino/soil_monitor.ino`
4. Select your Board (Uno/Nano/Mega) and Port (e.g., COM3, COM4)
5. Click Upload
6. **Important**: Update `ARDUINO_COM_PORT` in `config.py` to match your port

### 5. Run Application

**With Arduino (Real Sensors):**
```bash
python app.py
```
OR double-click: `run.bat`

**Demo Mode (No Arduino):**
```bash
python app_demo.py
```
OR double-click: `run_demo.bat`

### 6. Open Browser

http://localhost:5000

## 📁 Project Structure

```
soil-health-monitoring-system/
├── arduino/
│   └── soil_monitor.ino       # Arduino sensor code (NPK + DHT + Moisture)
├── templates/
│   └── index.html             # Web interface (HTML + CSS + JS)
├── app.py                     # Main application (with Arduino)
├── app_demo.py                # Demo mode (simulated sensors)
├── llm_analyzer.py            # AI analysis engine (Google Gemini)
├── sensor_reader.py           # Arduino serial communication
├── config.py                  # Configuration (API keys, COM port)
├── config.example.py          # Configuration template
├── requirements.txt           # Python dependencies
├── run.bat                    # Quick start with Arduino
├── run_demo.bat               # Quick start demo mode
└── README.md                  # This file
```

## 🎯 How It Works

```
Arduino Sensors → Serial (JSON) → Python Flask → Google Gemini AI → Farmer-Friendly Recommendations
```

### Data Flow

1. **Sensor Reading**: Arduino reads NPK (RS485 at 4800 baud), temperature & humidity (DHT11), soil moisture (analog)
2. **Data Transmission**: JSON format via USB serial at 9600 baud every 2 seconds
3. **User Input**: Farmer enters location, month, and desired crop via web interface
4. **AI Analysis**: Google Gemini 2.5 Flash analyzes soil data + crop requirements + location + season
5. **Smart Recommendations**: 
   - Crop suitability verdict (Excellent/Good/Moderate/Poor)
   - Nutrient deficiency analysis with specific values
   - Fertilizer plan (Urea, DAP, MOP) with exact kg/acre and timing
   - Irrigation schedule based on current moisture levels
   - Expected yield estimates and risk warnings
   - Alternative crop suggestions if needed

## 📊 Sample AI Analysis

**Input:**
- Location: Nashik, Maharashtra
- Month: November
- Crop: Cotton
- Sensor Data: N=35, P=22, K=180 mg/kg, Temp=28°C, Humidity=65%, Moisture=45%

**AI Output (Gemini 2.5 Flash):**

### Crop Suitability
Growing cotton in Nashik during November is Moderate. The temperature is suitable but winter cold may stress plants during flowering. Cotton is typically a Kharif crop (June-October), so November planting may face challenges with shorter daylight and cooler nights affecting boll development.

### Soil Nutrient Status
Your nitrogen level at 35 mg/kg is lower than the ideal range of 50-80 mg/kg for cotton by about 15-45 mg/kg. Phosphorus at 22 mg/kg is also below the recommended 30-50 mg/kg. Potassium at 180 mg/kg is within the good range of 150-250 mg/kg.

### Fertilizer Plan
1. Urea 65 kg per acre - Apply in three splits: first at sowing, second after 25 days, third at flowering stage
2. DAP 55 kg per acre - Apply before sowing to boost phosphorus
3. MOP 30 kg per acre - Apply at flowering stage for better boll quality

After fertilizers, ensure proper incorporation into soil and avoid over-application which can harm beneficial microbes.

### Irrigation Plan
Your soil moisture is at 45 percent which is moderate. Irrigate every 7 to 10 days depending on weather conditions. Cotton needs consistent moisture during flowering and boll formation stages. Reduce irrigation frequency during boll opening to prevent fiber damage and disease.

### Final Advice
You can proceed with cotton cultivation but expect moderate yields of 8-12 quintals per acre due to off-season planting. The major risk is cold stress during December-January which can reduce boll setting. Consider planting Rabi crops like wheat or chickpea which are better suited for November planting in Nashik.

## 🌾 Supported Crops

Works with **any crop**! Optimized for:
- **Kharif**: Cotton, Rice, Maize, Soybean, Groundnut
- **Rabi**: Wheat, Chickpea, Mustard, Barley
- **Fruits**: Mango, Banana, Pomegranate, Orange
- **Vegetables**: Tomato, Potato, Onion, Chili

## 🎓 Educational Use

Perfect for:
- College engineering projects (IoT, Embedded Systems)
- Agriculture technology demonstrations
- Smart farming research
- AI/ML application projects
- Final year projects

## 🛠️ Troubleshooting

### Sensor values show "--"
- Click "Start Reading Sensors" button in web interface
- Check Arduino is connected to correct COM port
- Update `ARDUINO_COM_PORT` in `config.py` to match your port
- Verify Arduino code is uploaded successfully
- **Important**: Close Arduino IDE Serial Monitor (it blocks the port!)

### "Failed to connect to Arduino" error
- Check USB cable connection
- Verify correct COM port in `config.py`
- Ensure Arduino drivers are installed
- Try different USB port
- Close any program using the serial port (Arduino IDE, PuTTY, etc.)

### Fallback mode appears instead of AI
- Check `config.py` has valid Gemini API key
- Ensure `USE_GEMINI = True` in config.py
- Verify internet connection is active
- Check terminal/console for specific error messages
- Verify API key is active at [Google AI Studio](https://aistudio.google.com/app/apikey)

### NPK values are 0 or not updating
- Normal if sensor probe is in air - insert into damp soil
- Check RS485 wiring: Module RXD → Arduino Pin 7, Module TXD → Arduino Pin 4
- Verify NPK sensor power supply (usually 5-12V)
- Confirm baud rate is 4800 in Arduino code
- Wait 5-10 seconds for sensor to stabilize

### Temperature/Humidity shows "nan" or "--"
- Check DHT11 wiring: VCC→5V, GND→GND, DATA→Pin 2
- Add 10kΩ pull-up resistor between DATA and VCC (recommended)
- Wait 2-3 seconds after power-on for sensor initialization
- Try replacing DHT11 sensor (they can fail over time)
- Ensure DHT library is installed in Arduino IDE

### Web page not loading
- Check if Flask server is running (should show "Running on http://127.0.0.1:5000")
- Verify no other application is using port 5000
- Try accessing http://localhost:5000 instead
- Check firewall settings
- Look for error messages in terminal/console

## 💡 Demo Mode

Test the complete system without Arduino:
- Simulated sensor data with realistic variations
- Full AI analysis capabilities
- Perfect for presentations and testing
- No hardware setup required

## 🌐 API Information

**Google Gemini API:**
- **Free Tier**: 60 requests per minute
- **Response Time**: 3-10 seconds
- **Cost**: $0 (free for this usage)
- **No credit card required**
- Get key: https://aistudio.google.com/app/apikey

## 📝 Configuration

Edit `config.py`:

```python
# AI Configuration
USE_GEMINI = True
GEMINI_API_KEY = "your-api-key-here"

# Arduino Configuration
ARDUINO_COM_PORT = "COM4"
ARDUINO_BAUDRATE = 9600
```

## 🎬 Demo Tips

**Before Presentation:**
- Upload Arduino code 30 minutes before
- Test all sensors
- Keep Arduino connected and powered
- Have demo mode ready as backup

**During Demo:**
1. Show real-time sensor updates
2. Touch moisture sensor to demonstrate live changes
3. Explain each sensor's agricultural purpose
4. Run AI analysis with real soil data
5. Highlight specific fertilizer recommendations

**If Hardware Fails:**
- Switch to `python app_demo.py`
- Same AI analysis with simulated data
- Seamless fallback

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

MIT License - Free to use for educational and commercial purposes

## 👨‍💻 Author

**Param Patel**
- GitHub: [@Param-Patel-o5](https://github.com/Param-Patel-o5)
- Project: Soil Health Monitoring System

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Arduino community for sensor libraries
- Flask framework for web development
- Indian agricultural research for crop data

## 🔮 Future Enhancements

- [ ] Mobile app (Android/iOS) for remote monitoring
- [ ] Historical data tracking with charts and analytics
- [ ] Multi-language support (Hindi, Marathi, Gujarati, etc.)
- [ ] Soil pH sensor integration
- [ ] Weather API integration for better predictions
- [ ] Crop disease detection using image recognition
- [ ] Market price recommendations for harvest planning
- [ ] SMS/WhatsApp notifications for critical alerts
- [ ] Database integration for multiple farm management
- [ ] Export reports as PDF
- [ ] Comparison with neighboring farms

## 📈 Project Status

**Current Version**: 1.0.0 (Production Ready)

**Completed Features**:
- ✅ Arduino sensor integration (NPK, DHT11, Soil Moisture)
- ✅ Real-time data reading via serial communication
- ✅ Flask web server with REST API
- ✅ Google Gemini AI integration
- ✅ Responsive web interface
- ✅ Demo mode for testing without hardware
- ✅ Fallback mode for offline operation
- ✅ Comprehensive error handling
- ✅ Complete documentation

**Tested With**:
- Arduino Uno/Nano
- NPK RS485 Sensor (4800 baud)
- DHT11 Temperature & Humidity Sensor
- Analog Soil Moisture Sensor
- Google Gemini 2.5 Flash API
- Windows/Linux/Mac systems

**Last Updated**: November 2024

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check existing issues for solutions
- Review troubleshooting section above
- Contact: [@Param-Patel-o5](https://github.com/Param-Patel-o5)

## 💰 Cost Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| Arduino Uno | ₹400-600 | One-time |
| NPK Sensor | ₹2000-3000 | One-time |
| DHT11 | ₹50-100 | One-time |
| Moisture Sensor | ₹50-100 | One-time |
| Google Gemini API | ₹0 | Free forever |
| **Total** | **₹2500-4000** | **One-time investment** |

## 🌟 Project Highlights

- ✅ **Real-time IoT monitoring** with 6 sensors updating every 2 seconds
- ✅ **AI-powered recommendations** using Google Gemini 2.5 Flash
- ✅ **Farmer-friendly interface** with simple language and clear guidance
- ✅ **Cost-effective solution** - Total hardware cost ₹2500-4000 (one-time)
- ✅ **Scalable architecture** - Easy to add more sensors or features
- ✅ **Open source** - Free to use, modify, and distribute
- ✅ **Production-ready** - Tested with real hardware and AI integration
- ✅ **Demo mode included** - Test without hardware
- ✅ **Fallback mode** - Works even without internet/API
- ✅ **Well-documented** - Complete setup guide and troubleshooting

---

**Made with ❤️ for Indian Farmers**

*Empowering agriculture through technology*

**Star ⭐ this repo if you find it helpful!**
