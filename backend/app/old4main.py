import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# --- ADD THESE FOR GEOPY TO WORK ---
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

OLLAMA_API_URL = "http://localhost:11434/api/generate"

app = FastAPI()

# Enable CORS for your local React project server profiles
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    prompt: str

async def fetch_open_meteo_weather(city_name: str) -> dict:
    """
    Bypasses the blocked Open-Meteo geocoding subdomain by routing 
    the text extraction through OpenStreetMap data layers natively.
    """
    try:
        # Initialize geolocator with a custom unique user agent string
        geolocator = Nominatim(user_agent="videxpulse_weather_agent_hub_v1")
        
        # Append ', Tamil Nadu, India' to target small regional towns accurately
        search_query = f"{city_name.lower()}, Tamil Nadu, India"
        location = geolocator.geocode(search_query, timeout=10)
        
        if not location:
            return {"error": f"Geocoding framework could not locate spatial coordinates for: '{city_name}'"}
            
        lat = location.latitude
        lon = location.longitude
        
        # Query Open-Meteo core forecast API using the resolved coordinates
        forecast_url = f"https://open-meteo.com{lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"
        
        async with httpx.AsyncClient() as client:
            forecast_res = await client.get(forecast_url, timeout=10.0)
            
            try:
                forecast_data = forecast_res.json()
            except Exception:
                return {"error": f"Forecast server returned non-JSON structure. Raw: {forecast_res.text[:100]}"}
                
            return {
                "latitude": lat,
                "longitude": lon,
                "timezone": forecast_data.get("timezone"),
                "daily_forecast": forecast_data.get("daily", {})
            }
            
    except (GeocoderTimedOut, GeocoderServiceError):
        return {"error": "The Geocoding service timed out. Please check your Mac mini network connection and try again."}
    except Exception as e:
        return {"error": f"Pipeline execution failure: {str(e)}"}

@app.post("/api/chat")
async def handle_weather_query(request: QueryRequest):
    # 1. Forward the query to your local 4-bit model build
    payload = {
        "model": "videxpulse-weather-agent",
        "prompt": request.prompt,
        "stream": False
    }
    
    async with httpx.AsyncClient() as client:
        try:
            ollama_response = await client.post(OLLAMA_API_URL, json=payload, timeout=30.0)
            model_output = ollama_response.json().get("response", "").strip()
            
            # 2. Extract and parse the exact JSON tool call your model generated
            tool_calls = json.loads(model_output)
            
            if isinstance(tool_calls, list) and len(tool_calls) > 0:
                first_call = tool_calls[0]
                function_args = first_call.get("function", {}).get("arguments", "{}")
                
                if isinstance(function_args, str):
                    function_args = json.loads(function_args)
                
                target_city = function_args.get("city_name")
                
                if target_city:
                    # 3. Securely execute the alternative open-source lookup
                    live_weather_data = await fetch_open_meteo_weather(target_city)
                    return {
                        "status": "success",
                        "city": target_city,
                        "tool_triggered": "fetch_imd_city_forecast", # Keep this constant to not break your UI state
                        "data": live_weather_data
                    }
            
            return {"status": "fallback", "message": "Model did not trigger a known tool mapping.", "raw": model_output}
            
        except json.JSONDecodeError:
            return {"status": "error", "message": "Failed to parse structural tool calling array.", "raw_output": model_output}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
