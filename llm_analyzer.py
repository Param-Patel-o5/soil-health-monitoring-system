import requests
import json
import os

class SoilAnalyzer:
    def __init__(self, use_gemini=True, gemini_api_key=None):
        """Initialize LLM analyzer with Google Gemini"""
        self.use_gemini = use_gemini
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        
    def analyze_soil(self, sensor_data, farmer_input, weather_data=None):
        """Analyze soil data and provide recommendations"""
        
        # Build context prompt with weather data
        prompt = self._build_short_prompt(sensor_data, farmer_input, weather_data)
        
        # Try Google Gemini first if enabled
        if self.use_gemini and self.gemini_api_key:
            try:
                # Shorter, optimized prompt for faster response
                short_prompt = self._build_short_prompt(sensor_data, farmer_input)
                
                response = requests.post(
                    f"{self.gemini_url}?key={self.gemini_api_key}",
                    json={
                        "contents": [{
                            "parts": [{"text": short_prompt}]
                        }],
                        "generationConfig": {
                            "temperature": 0.8,
                            "maxOutputTokens": 8000,
                            "topP": 0.95,
                            "topK": 40,
                            "responseModalities": ["TEXT"]
                        },
                        "systemInstruction": {
                            "parts": [{"text": "Respond directly without extended thinking. Provide concise, practical analysis."}]
                        }
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    try:
                        content = result['candidates'][0]['content']
                        finish_reason = result['candidates'][0].get('finishReason', 'UNKNOWN')
                        
                        if 'parts' in content and len(content['parts']) > 0:
                            ai_response = content['parts'][0]['text']
                            
                            # Check if response was cut off
                            if finish_reason == 'MAX_TOKENS':
                                ai_response += "\n\n[Note: Response was truncated due to length. The analysis covers the most critical aspects.]"
                            
                            # Return clean response without header
                            return ai_response
                        else:
                            print(f"Gemini returned no text (only thinking tokens)")
                            print(f"Response: {result}")
                            # Fall through to fallback
                            return self._fallback_analysis(sensor_data, farmer_input)
                    except (KeyError, IndexError) as e:
                        print(f"Gemini response parsing error: {e}")
                        print(f"Response: {result}")
                        # Fall through to fallback
                        return self._fallback_analysis(sensor_data, farmer_input)
                else:
                    print(f"Gemini API error: {response.status_code} - {response.text}")
                    # Fall through to fallback
                    return self._fallback_analysis(sensor_data, farmer_input)
            except Exception as e:
                print(f"Gemini error: {e}")
                # Fall through to fallback
                return self._fallback_analysis(sensor_data, farmer_input)
        
        # If Gemini fails, use fallback
        return self._fallback_analysis(sensor_data, farmer_input)
    

    
    def _build_short_prompt(self, sensor_data, farmer_input, weather_data=None):
        """Build shorter, faster prompt for Gemini with optional weather integration"""
        crop = farmer_input.get('crop', 'the crop')
        location = farmer_input.get('location', 'the location')
        month = farmer_input.get('month', 'this month')
        
        temp = sensor_data.get('temp', 'N/A')
        humidity = sensor_data.get('humidity', 'N/A')
        moisture = sensor_data.get('moisture', 'N/A')
        nitrogen = sensor_data.get('nitrogen', 'N/A')
        phosphorus = sensor_data.get('phosphorus', 'N/A')
        potassium = sensor_data.get('potassium', 'N/A')
        
        # Build weather context only if available
        weather_context = ""
        weather_instructions = ""
        
        if weather_data:
            try:
                from weather_service import WeatherService
                ws = WeatherService(None)
                weather_context = ws.format_for_prompt(weather_data)
                weather_instructions = " Use the live weather data to provide more accurate irrigation timing and fertilizer application advice. If rain is forecasted, adjust irrigation recommendations. If temperature extremes are expected, warn about stress risks."
            except Exception as e:
                # Weather formatting failed, continue without it
                weather_context = ""
                weather_instructions = ""
        
        prompt = f"""You are an agricultural advisor who explains things in simple, practical farmer-friendly language. A farmer wants to grow {crop} in {location} during {month}. Use the data below to give a clear and helpful analysis.

SOIL DATA
Temperature: {temp} °C
Humidity: {humidity} %
Soil Moisture: {moisture} %
Nitrogen: {nitrogen} mg/kg
Phosphorus: {phosphorus} mg/kg
Potassium: {potassium} mg/kg
{weather_context}

Give the answer in FIVE sections. Start each section with a heading in this exact format: <h3>Heading Name</h3>. Write in simple paragraphs. Do NOT use hashtags, asterisks, hyphens, or bullet points anywhere except for fertilizer numbering.

<h3>Crop Suitability</h3>
Explain if growing {crop} in {location} during {month} is Excellent, Good, Moderate, or Poor. Give the main reason in 2-3 sentences. If weather data is available, adjust for rain, heat or cold. Mention stress or irrigation needs if required.

<h3>Soil Nutrient Status</h3>
Compare the NPK values with the ideal range for {crop}. Say which nutrients are low or high and by how much in 2-3 sentences. Use natural language like Nitrogen is lower than the ideal level by around X mg/kg.

<h3>Fertilizer Plan</h3>
Write the fertilizer plan in numbered points (1, 2, 3) with exact amounts in kg per acre and timing. For example:
1. Urea 60 kg per acre - Apply in three splits: first at sowing, second after 20 days, third at flowering stage
2. DAP 50 kg per acre - Apply before sowing
3. MOP 40 kg per acre - Apply at flowering stage

After fertilizers, add any important notes about nutrient management in one sentence.

<h3>Irrigation Plan</h3>
Write about irrigation in a paragraph. Be specific based on the soil moisture value of {moisture} percent. If moisture is high (above 800), say wait X days before first irrigation. If moisture is medium (400-800), say irrigate every X days. If moisture is low (below 400), say irrigate immediately and then every X days. Mention critical stages when water is most needed like flowering, boll formation, etc.

<h3>Final Advice</h3>
Tell the farmer whether they should go ahead in 2-3 sentences. Mention the expected yield range based on the conditions. Add one major risk. Suggest one alternative crop if this crop is not ideal.

Keep the explanation helpful, simple and personalised. Use numbered points only for fertilizers. Use <h3> tags for all headings. Everything else should be plain paragraphs. Avoid technical terms unless needed."""
        
        return prompt
    
    def _fallback_analysis(self, sensor_data, farmer_input):
        """Rule-based analysis when LLM is unavailable"""
        crop = farmer_input.get('crop', 'crop').lower()
        month = farmer_input.get('month', 'N/A')
        location = farmer_input.get('location', 'N/A')
        
        temp = sensor_data.get('temp', 0)
        moisture = sensor_data.get('moisture', 0)
        nitrogen = sensor_data.get('nitrogen', 0)
        phosphorus = sensor_data.get('phosphorus', 0)
        potassium = sensor_data.get('potassium', 0)
        
        analysis = f"""🌾 SOIL HEALTH ANALYSIS REPORT
{'='*60}

📍 Location: {location}
📅 Month: {month}
🌱 Desired Crop: {farmer_input.get('crop', 'N/A')}

📊 SENSOR READINGS:
- Temperature: {temp}°C
- Soil Moisture: {moisture}%
- Nitrogen (N): {nitrogen} mg/kg
- Phosphorus (P): {phosphorus} mg/kg
- Potassium (K): {potassium} mg/kg

{'='*60}

✅ SOIL SUITABILITY ASSESSMENT:
"""
        
        # Temperature assessment
        if 20 <= temp <= 35:
            analysis += f"✓ Temperature ({temp}°C) is suitable for most crops\n"
        elif temp < 20:
            analysis += f"⚠ Temperature ({temp}°C) is LOW - may slow growth\n"
        else:
            analysis += f"⚠ Temperature ({temp}°C) is HIGH - may stress plants\n"
        
        # Moisture assessment
        if 40 <= moisture <= 60:
            analysis += f"✓ Soil moisture ({moisture}%) is optimal\n"
        elif moisture < 40:
            analysis += f"⚠ Soil moisture ({moisture}%) is LOW - irrigation needed\n"
        else:
            analysis += f"⚠ Soil moisture ({moisture}%) is HIGH - drainage needed\n"
        
        # NPK assessment
        analysis += "\n🧪 NUTRIENT ANALYSIS:\n"
        
        if nitrogen < 30:
            analysis += f"⚠ Nitrogen ({nitrogen} mg/kg) is LOW\n"
        elif nitrogen > 50:
            analysis += f"✓ Nitrogen ({nitrogen} mg/kg) is GOOD\n"
        else:
            analysis += f"○ Nitrogen ({nitrogen} mg/kg) is MODERATE\n"
        
        if phosphorus < 20:
            analysis += f"⚠ Phosphorus ({phosphorus} mg/kg) is LOW\n"
        elif phosphorus > 35:
            analysis += f"✓ Phosphorus ({phosphorus} mg/kg) is GOOD\n"
        else:
            analysis += f"○ Phosphorus ({phosphorus} mg/kg) is MODERATE\n"
        
        if potassium < 150:
            analysis += f"⚠ Potassium ({potassium} mg/kg) is LOW\n"
        elif potassium > 200:
            analysis += f"✓ Potassium ({potassium} mg/kg) is GOOD\n"
        else:
            analysis += f"○ Potassium ({potassium} mg/kg) is MODERATE\n"
        
        # Fertilizer recommendations
        analysis += f"\n💊 FERTILIZER RECOMMENDATIONS:\n"
        
        if nitrogen < 40:
            analysis += "• UREA (46% N): Apply 50-75 kg/acre\n"
            analysis += "  Frequency: Split into 2-3 doses during growing season\n"
        
        if phosphorus < 25:
            analysis += "• DAP (18-46-0): Apply 40-60 kg/acre\n"
            analysis += "  Frequency: Apply at sowing/planting time\n"
        
        if potassium < 180:
            analysis += "• MOP (Muriate of Potash): Apply 30-50 kg/acre\n"
            analysis += "  Frequency: Apply before flowering stage\n"
        
        # Crop-specific advice
        analysis += f"\n🌾 CROP-SPECIFIC ADVICE FOR {farmer_input.get('crop', 'YOUR CROP').upper()}:\n"
        
        if 'cotton' in crop:
            analysis += "• Cotton requires well-drained soil with pH 6.0-7.5\n"
            analysis += "• Best season: Kharif (June-October)\n"
            analysis += "• Ensure adequate potassium for fiber quality\n"
        elif 'wheat' in crop:
            analysis += "• Wheat prefers cool weather (15-25°C)\n"
            analysis += "• Best season: Rabi (November-March)\n"
            analysis += "• Requires good nitrogen supply\n"
        elif 'rice' in crop:
            analysis += "• Rice needs high moisture (standing water)\n"
            analysis += "• Best season: Kharif (June-October)\n"
            analysis += "• Requires consistent water supply\n"
        elif 'kiwi' in crop:
            analysis += "• Kiwi needs cool winters and warm summers\n"
            analysis += "• Requires well-drained, slightly acidic soil\n"
            analysis += "• Not suitable for all regions in India\n"
        else:
            analysis += f"• Ensure soil conditions match {farmer_input.get('crop', 'crop')} requirements\n"
            analysis += "• Consult local agricultural extension office\n"
        
        # Seasonal advice
        analysis += f"\n📅 SEASONAL CONSIDERATIONS ({month}):\n"
        if month in ['June', 'July', 'August', 'September']:
            analysis += "• Kharif season - good for rice, cotton, maize\n"
            analysis += "• Monsoon period - ensure proper drainage\n"
        elif month in ['October', 'November', 'December', 'January', 'February', 'March']:
            analysis += "• Rabi season - good for wheat, mustard, chickpea\n"
            analysis += "• Cooler weather - monitor irrigation\n"
        else:
            analysis += "• Summer season - ensure adequate irrigation\n"
            analysis += "• Consider heat-tolerant varieties\n"
        
        # Additional tips
        analysis += f"\n💡 ADDITIONAL RECOMMENDATIONS:\n"
        analysis += "• Add organic matter (compost/FYM) to improve soil structure\n"
        analysis += "• Test soil pH - most crops prefer 6.0-7.5\n"
        analysis += "• Practice crop rotation to maintain soil health\n"
        analysis += "• Consider mulching to retain moisture\n"
        
        analysis += f"\n{'='*60}\n"
        analysis += "⚠️ FALLBACK MODE: This is a basic rule-based analysis.\n"
        analysis += "🤖 For AI-powered intelligent analysis:\n"
        analysis += "   • Check if Google Gemini API key is set in config.py\n"
        analysis += "   • Ensure internet connection is active\n"
        analysis += "   • Verify USE_GEMINI = True in config.py\n"
        
        return analysis
