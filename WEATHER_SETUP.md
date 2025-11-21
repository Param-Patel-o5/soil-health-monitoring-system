# 🌤️ Weather API Integration Setup

## Why Add Weather Data?

Integrating live weather significantly improves AI recommendation accuracy:

✅ **Better Irrigation Advice** - If rain is forecasted, system advises to delay irrigation
✅ **Pest/Disease Warnings** - High humidity + temperature = fungal disease risk
✅ **Planting Timing** - Checks if weather suits crop in next 7-14 days
✅ **Fertilizer Application** - Advises best timing based on rainfall forecast
✅ **Real-time Climate Context** - Actual conditions vs assumptions

## Quick Setup (2 minutes)

### 1. Get Free API Key

1. Go to: https://openweathermap.org/api
2. Click "Sign Up" (top right)
3. Create free account
4. Go to "API keys" tab
5. Copy your API key

### 2. Add to Config

Open `config.py` and update:

```python
USE_WEATHER_API = True
OPENWEATHER_API_KEY = "your-api-key-here"  # Paste your key
```

### 3. Test It

Run the demo:
```bash
python app_demo.py
```

Enter location like "Pune" or "Delhi" - you'll see weather data in terminal!

## What Data is Fetched?

**Current Weather:**
- Temperature & feels like
- Humidity
- Recent rainfall (last 3 hours)
- Wind speed
- Weather conditions

**3-Day Forecast:**
- Average temperature
- Average humidity
- Rain expected (Yes/No)
- Total expected rainfall

## How It Improves AI Responses

**Without Weather:**
> "Apply 60 kg/acre Urea. Irrigate every 7 days."

**With Weather:**
> "Apply 60 kg/acre Urea. However, 15mm rain is forecasted in next 2 days, so delay irrigation until soil moisture drops below 40%. Apply first Urea dose after the rain to maximize nutrient uptake."

## API Limits (Free Tier)

- **1000 calls per day** (more than enough)
- **60 calls per minute**
- **No credit card required**
- **Forever free**

## Example Enhanced Output

```
LIVE WEATHER DATA:
Current Conditions:
- Temperature: 28.5°C (Feels like: 31°C)
- Humidity: 65%
- Weather: partly cloudy
- Wind Speed: 3.2 m/s
- Recent Rainfall: 0 mm (last 3 hours)

3-Day Forecast:
- Average Temperature: 29.2°C
- Average Humidity: 68%
- Rain Expected: Yes
- Expected Rainfall: 12.5 mm

AI Analysis:
"Growing cotton in Pune during November is suitable. Current temperature 
of 28.5°C is ideal for cotton growth. However, with 12.5mm rain expected 
in next 3 days and current soil moisture at 45%, hold off on irrigation. 
The forecasted rain will naturally replenish soil moisture. Apply first 
dose of Urea (20 kg/acre) immediately after the rain stops, as moist soil 
improves nitrogen absorption..."
```

## Troubleshooting

**Issue: Weather data not showing**
- Check if `USE_WEATHER_API = True`
- Verify API key is correct
- Ensure internet connection
- Check terminal for error messages

**Issue: "Weather API error: 401"**
- API key is invalid
- Get new key from OpenWeatherMap

**Issue: "Weather API error: 404"**
- Location name not found
- Try different spelling (e.g., "Mumbai" instead of "Bombay")

## Cost Analysis

**Free Tier:**
- 1000 calls/day = enough for 1000 farmers per day
- Perfect for college projects and small deployments

**If you need more:**
- Paid plans start at $40/month for 100,000 calls
- Not needed for academic projects

## Privacy Note

Weather API only sends location name (city), not exact coordinates or personal data.
