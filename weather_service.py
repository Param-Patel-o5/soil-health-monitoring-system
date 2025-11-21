import requests
from datetime import datetime

class WeatherService:
    def __init__(self, api_key):
        """Initialize weather service with OpenWeatherMap API"""
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_weather_data(self, location):
        """Get current weather and forecast for location (fails gracefully)"""
        if not self.api_key or self.api_key == "YOUR_OPENWEATHER_API_KEY":
            return None
        
        # Clean location name and try multiple formats
        location = location.strip().title()  # "nashik" -> "Nashik"
        
        # Try different location formats
        location_formats = [
            f"{location},IN",
            f"{location},India",
            location
        ]
            
        try:
            current_data = None
            # Try each format until one works
            for loc_format in location_formats:
                try:
                    current_url = f"{self.base_url}/weather?q={loc_format}&appid={self.api_key}&units=metric"
                    current_response = requests.get(current_url, timeout=5)
                    
                    if current_response.status_code == 200:
                        current_data = current_response.json()
                        break
                except:
                    continue
            
            if not current_data:
                return None
            
            # Get 5-day forecast (optional, don't fail if this doesn't work)
            forecast_data = None
            try:
                # Use the same location format that worked for current weather
                for loc_format in location_formats:
                    try:
                        forecast_url = f"{self.base_url}/forecast?q={loc_format}&appid={self.api_key}&units=metric"
                        forecast_response = requests.get(forecast_url, timeout=5)
                        if forecast_response.status_code == 200:
                            forecast_data = forecast_response.json()
                            break
                    except:
                        continue
            except:
                pass  # Forecast is nice-to-have
            
            return self._parse_weather_data(current_data, forecast_data)
            
        except Exception as e:
            # Weather API failed - not critical, continue without it
            return None
    
    def _parse_weather_data(self, current, forecast):
        """Parse and structure weather data"""
        weather_info = {
            'current': {
                'temperature': current['main']['temp'],
                'feels_like': current['main']['feels_like'],
                'humidity': current['main']['humidity'],
                'pressure': current['main']['pressure'],
                'weather': current['weather'][0]['description'],
                'wind_speed': current['wind']['speed'],
                'clouds': current['clouds']['all']
            }
        }
        
        # Add rainfall data if available
        if 'rain' in current:
            weather_info['current']['rainfall_1h'] = current['rain'].get('1h', 0)
            weather_info['current']['rainfall_3h'] = current['rain'].get('3h', 0)
        else:
            weather_info['current']['rainfall_1h'] = 0
            weather_info['current']['rainfall_3h'] = 0
        
        # Parse forecast for next 7 days
        if forecast:
            weather_info['forecast'] = self._parse_forecast(forecast)
        
        return weather_info
    
    def _parse_forecast(self, forecast_data):
        """Parse 5-day forecast data"""
        forecast_summary = {
            'next_3_days': [],
            'rain_expected': False,
            'avg_temp': 0,
            'avg_humidity': 0,
            'total_rainfall': 0
        }
        
        temps = []
        humidities = []
        total_rain = 0
        
        # Process forecast (3-hour intervals for 5 days)
        for item in forecast_data['list'][:24]:  # Next 3 days (8 intervals per day)
            temp = item['main']['temp']
            humidity = item['main']['humidity']
            temps.append(temp)
            humidities.append(humidity)
            
            # Check for rain
            if 'rain' in item:
                rain_amount = item['rain'].get('3h', 0)
                total_rain += rain_amount
                if rain_amount > 0:
                    forecast_summary['rain_expected'] = True
            
            # Add daily summary
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            forecast_summary['next_3_days'].append({
                'date': date,
                'temp': temp,
                'humidity': humidity,
                'weather': item['weather'][0]['description']
            })
        
        forecast_summary['avg_temp'] = round(sum(temps) / len(temps), 1)
        forecast_summary['avg_humidity'] = round(sum(humidities) / len(humidities), 1)
        forecast_summary['total_rainfall'] = round(total_rain, 1)
        
        return forecast_summary
    
    def format_for_prompt(self, weather_data):
        """Format weather data for AI prompt - concise version"""
        if not weather_data:
            return ""
        
        current = weather_data['current']
        prompt_text = f"""
LIVE WEATHER: {current['temperature']}°C, {current['weather']}, Humidity {current['humidity']}%"""
        
        if 'forecast' in weather_data:
            forecast = weather_data['forecast']
            rain_info = f", Rain expected: {forecast['total_rainfall']}mm" if forecast['rain_expected'] else ", No rain expected"
            prompt_text += f""", Next 3 days: {forecast['avg_temp']}°C avg{rain_info}"""
        
        return prompt_text
