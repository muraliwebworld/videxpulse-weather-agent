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

import os
import subprocess
import json
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

async def fetch_weather_api_data(city_name: str) -> dict:
    """
    Queries WeatherAPI's real-time endpoint, extracting current metrics
    safely using native system curl calls.
    """
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return {"error": "Missing 'WEATHER_API_KEY' in local .env configuration."}
            
        clean_city = city_name.lower().strip()
        search_query = urllib.parse.quote(f"{clean_city}, India")
        
        # Point to the current.json endpoint since it matches your active free plan tier
        target_url = f"http://weatherapi.com{api_key}&q={search_query}&aqi=no"
        
        curl_cmd = [
            "curl", "-s", "--connect-timeout", "10", target_url
        ]
        
        system_process = subprocess.run(curl_cmd, capture_output=True, text=True)
        
        if system_process.returncode != 0:
            return {"error": f"Terminal curl execution dropped packet. Code: {system_process.returncode}"}
            
        try:
            weather_data = json.loads(system_process.stdout)
        except Exception:
            return {"error": "Endpoint returned non-JSON structure."}
            
        if "error" in weather_data:
            return {"error": f"WeatherAPI Error: {weather_data['error'].get('message')}"}
            
        current_data = weather_data.get("current", {})
        condition_data = current_data.get("condition", {})
        
        # Construct a standardized real-time data card for your React state mapping
        return {
            "is_current_only": True,
            "temp_c": current_data.get("temp_c", "--"),
            "feelslike_c": current_data.get("feelslike_c", "--"),
            "humidity": current_data.get("humidity", "--"),
            "wind_kph": current_data.get("wind_kph", "--"),
            "condition_text": condition_data.get("text", "Unknown"),
            "condition_icon": condition_data.get("icon", "")
        }
        
    except Exception as e:
        return {"error": f"WeatherAPI parsing error layout exception: {str(e)}"}

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
