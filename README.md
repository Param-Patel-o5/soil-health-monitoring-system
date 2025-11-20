# 🌱 Soil Health Monitoring System

AI-powered soil health monitoring system using Arduino sensors and Google Gemini. Provides real-time NPK analysis and crop-specific fertilizer recommendations for Indian farmers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Arduino](https://img.shields.io/badge/Arduino-Compatible-teal.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

This project combines IoT hardware (Arduino + sensors) with AI (Google Gemini) to help farmers make informed decisions about soil health and crop management. The system reads real-time soil parameters and provides detailed, actionable recommendations.

### Key Features

- **Real-time Monitoring**: Continuous reading of 6 soil parameters
- **AI-Powered Analysis**: Google Gemini 2.5 Flash for intelligent recommendations
- **Crop-Specific Advice**: Tailored suggestions based on crop type, location, and season
- **Fertilizer Recommendations**: Exact quantities (kg/acre) for Urea, DAP, MOP, etc.
- **Seasonal Guidance**: Kharif/Rabi/Zaid season suitability analysis
- **Web Interface**: Clean, responsive UI for easy interaction
- **Demo Mode**: Test without Arduino hardware

## 🔧 Hardware Requirements

- Arduino (Uno/Nano/Mega)
- NPK Sensor (Nitrogen, Phosphorus, Potassium)
- DHT11/DHT22 (Temperature & Humidity)
- Soil Moisture Sensor
- USB Cable for Serial Connection

## 💻 Software Requirements

- Python 3.8 or higher
- Arduino IDE
- Google Gemini API Key (free)
- Internet connection (for AI analysis)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Param-Patel-o5/soil-health-monitoring-system.git
cd soil-health-monitoring-system
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or use the automated installer:
```bash
install.bat
```

### 3. Get Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### 4. Configure the System

Open `config.py` and add your API key:

```python
USE_GEMINI = True
GEMINI_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual key
```

### 5. Run Demo Mode (No Arduino Required)

```bash
python app_demo.py
```

Or double-click:
```
run_demo.bat
```

Open browser: http://localhost:5000

### 6. Run with Arduino (Hardware Mode)

1. Upload `arduino/soil_monitor.ino` to your Arduino
2. Update COM port in `app.py` (line 9)
3. Run:

```bash
python app.py
```

Or double-click:
```
run.bat
```

## 📁 Project Structure

```
soil-health-monitoring-system/
├── arduino/
│   └── soil_monitor.ino          # Arduino sensor code
├── templates/
│   └── index.html                # Web interface
├── app.py                        # Main application (with Arduino)
├── app_demo.py                   # Demo mode (simulated sensors)
├── llm_analyzer.py               # AI analysis engine
├── sensor_reader.py              # Arduino serial communication
├── config.py                     # Configuration file
├── requirements.txt              # Python dependencies
├── install.bat                   # Automated installer
├── run.bat                       # Run with Arduino
├── run_demo.bat                  # Run demo mode
└── README.md                     # This file
```

## 🎯 How It Works

1. **Sensor Reading**: Arduino reads soil parameters (NPK, moisture, temperature, humidity)
2. **Data Transmission**: Sensor data sent to laptop via USB serial
3. **User Input**: Farmer enters location, month, and desired crop
4. **AI Analysis**: Google Gemini analyzes soil data + farmer inputs
5. **Recommendations**: System provides:
   - Soil suitability verdict
   - Nutrient deficiency analysis
   - Exact fertilizer quantities
   - Irrigation schedule
   - Seasonal advice
   - Expected yield predictions

## 📊 Sample Output

```
Growing Cotton in Pune during November is suitable. The soil shows moderate 
nitrogen levels at 35 mg/kg, which is below the ideal range of 60-80 mg/kg 
for cotton. Apply 60 kg/acre of Urea in 3 splits: 20 kg at sowing, 20 kg 
after 30 days, and 20 kg before flowering. Current moisture at 45% is optimal. 
Irrigate every 7 days during vegetative stage...
```

## 🌾 Supported Crops

The system provides analysis for any crop, with optimized recommendations for:
- Cotton, Wheat, Rice, Maize
- Sugarcane, Soybean, Groundnut
- Mango, Banana, Pomegranate
- Tomato, Potato, Onion
- And many more...

## 🔬 Sensor Specifications

| Sensor | Parameter | Range | Unit |
|--------|-----------|-------|------|
| NPK Sensor | Nitrogen | 0-100 | mg/kg |
| NPK Sensor | Phosphorus | 0-100 | mg/kg |
| NPK Sensor | Potassium | 0-200 | mg/kg |
| DHT11/22 | Temperature | 0-50 | °C |
| DHT11/22 | Humidity | 20-90 | % |
| Moisture | Soil Moisture | 0-100 | % |

## 🎓 Educational Use

This project is ideal for:
- College engineering projects
- IoT and embedded systems courses
- Agriculture technology demonstrations
- Smart farming research
- AI/ML application projects

## 🛠️ Troubleshooting

### Issue: "Fallback Mode" appears instead of AI analysis
**Solution**: 
- Check if `USE_GEMINI = True` in config.py
- Verify your API key is correct
- Ensure internet connection is active

### Issue: Sensor values show "--"
**Solution**:
- Click "Start Reading Sensors" button
- Check Arduino USB connection
- Verify COM port in app.py

### Issue: Arduino not detected
**Solution**:
- Open Device Manager (Windows)
- Check "Ports (COM & LPT)"
- Update COM port in app.py

## 💡 Demo Mode Features

Test the system without Arduino:
- Simulated sensor data with realistic variations
- All AI analysis features work
- Perfect for presentations and testing
- No hardware setup required

## 🌐 API Usage

Google Gemini API:
- **Free Tier**: 60 requests per minute
- **Response Time**: 3-10 seconds
- **Cost**: $0 (free for this usage)
- **No credit card required**

## 📝 Configuration Options

Edit `config.py`:

```python
# Enable/disable AI analysis
USE_GEMINI = True

# Your Google Gemini API key
GEMINI_API_KEY = "your-key-here"

# Arduino COM port (for hardware mode)
ARDUINO_COM_PORT = "COM3"
ARDUINO_BAUDRATE = 9600
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Param Patel**
- GitHub: [@Param-Patel-o5](https://github.com/Param-Patel-o5)

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Arduino community for sensor libraries
- Flask framework for web interface
- Indian agricultural research for crop data

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

## 🔮 Future Enhancements

- [ ] Mobile app integration
- [ ] Historical data tracking
- [ ] Multi-language support
- [ ] Soil pH sensor integration
- [ ] Weather API integration
- [ ] Crop disease detection
- [ ] Market price recommendations

---

**Made with ❤️ for Indian Farmers**

*Empowering agriculture through technology*
