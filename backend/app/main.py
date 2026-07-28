import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

OLLAMA_API_URL = "http://localhost:11434/api/generate"

app = FastAPI()

# Enable CORS configurations for local React development ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    prompt: str

async def fetch_weather_api_data(city_name: str) -> dict:
    """Queries WeatherAPI.com using your exact secure HTTPS pipeline keys."""
    # Hardcoded your active token string directly to prevent local file reading bugs
    api_key = "46924e5c14644a3395f180201262807"
    clean_city = city_name.lower().strip()
    
    # Secure HTTPS endpoint protocol format layout 
    target_url = "https://api.weatherapi.com/v1/current.json"
    query_params = {
        "key": api_key,
        "q": f"{clean_city}, India",
        "aqi": "no"
    }
    
    print(f"\n📡 [DEBUG] Sending request to WeatherAPI...")
    print(f"   URL: {target_url}")
    print(f"   Query Target Parameter: q='{query_params['q']}'")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, params=query_params, timeout=10.0)
            print(f"📥 [DEBUG] WeatherAPI Response Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"⚠️ [DEBUG] Raw Error Payload: {response.text[:200]}")
                return {"error": f"WeatherAPI Service returned HTTP Status {response.status_code}"}
                
            weather_data = response.json()
            
            if "error" in weather_data:
                print(f"❌ [DEBUG] WeatherAPI internal structural JSON error: {weather_data['error']}")
                return {"error": f"WeatherAPI Error Payload: {weather_data['error'].get('message')}"}
                
            current_data = weather_data.get("current", {})
            condition_data = current_data.get("condition", {})
            
            print(f"✅ [DEBUG] Successfully parsed real-time data frame for: {clean_city}")
            return {
                "temp_c": current_data.get("temp_c", "--"),
                "feelslike_c": current_data.get("feelslike_c", "--"),
                "humidity": current_data.get("humidity", "--"),
                "wind_kph": current_data.get("wind_kph", "--"),
                "condition_text": condition_data.get("text", "Unknown"),
                "condition_icon": condition_data.get("icon", "")
            }
            
        except httpx.RequestError as e:
            print(f"💥 [DEBUG] Transport Exception caught: {str(e)}")
            return {"error": f"Network transport linkage dropped: {str(e)}"}
        except Exception as e:
            print(f"💥 [DEBUG] Unexpected runtime parsing exception: {str(e)}")
            return {"error": f"Failed parsing real-time service endpoints: {str(e)}"}

@app.post("/api/chat")
async def handle_weather_query(request: QueryRequest):
    print(f"\n📥 [DEBUG] Received user frontend text prompt: '{request.prompt}'")
    
    payload = {
        "model": "videxpulse-weather-agent",
        "prompt": request.prompt,
        "stream": False
    }
    
    async with httpx.AsyncClient() as client:
        try:
            ollama_response = await client.post(OLLAMA_API_URL, json=payload, timeout=30.0)
            model_output = ollama_response.json().get("response", "").strip()
            
            print("🧠 [DEBUG] Raw local Ollama agent inference output string:")
            print(f"   {model_output}")
            
            tool_calls = json.loads(model_output)
            
            if isinstance(tool_calls, list) and len(tool_calls) > 0:
                first_call = tool_calls[0]
                function_args = first_call.get("function", {}).get("arguments", "{}")
                
                if isinstance(function_args, str):
                    function_args = json.loads(function_args)
                
                target_city = function_args.get("city_name")
                print(f"🎯 [DEBUG] Model matched tool routing target city parameter: '{target_city}'")
                
                if target_city:
                    live_weather_data = await fetch_weather_api_data(target_city)
                    return {
                        "status": "success",
                        "city": target_city,
                        "tool_triggered": "fetch_imd_city_forecast",
                        "data": live_weather_data,
                        "raw_json": model_output 
                    }
            
            print("⚠️ [DEBUG] Model response did not trace an active list layout matching templates.")
            return {"status": "fallback", "message": "Model didn't trigger a tool matching expectations.", "raw": model_output}
            
        except json.JSONDecodeError:
            print("❌ [DEBUG] Model structure failed clean text string to JSON extraction parse lines.")
            return {"status": "fallback", "message": "Model output format broke JSON parsing structure rules.", "raw": model_output}
        except Exception as e:
            print(f"💥 [DEBUG] Internal app routing pipeline failure exception: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
