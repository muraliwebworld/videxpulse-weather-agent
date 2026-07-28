import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Secure your official IMD token in a local .env file
IMD_JWT_TOKEN = os.getenv("IMD_JWT_TOKEN")
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

async def fetch_imd_weather_data(city_name: str) -> dict:
    """Hits the live official IMD server safely away from the public browser."""
    url = f"https://imd.gov.in/{city_name.lower()}"
    headers = {
        "Authorization": f"Bearer {IMD_JWT_TOKEN}",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            return {"error": f"IMD server returned HTTP status {response.status_code}"}
        except Exception as e:
            return {"error": f"Failed connecting to IMD endpoint: {str(e)}"}

@app.post("/api/chat")
async def handle_weather_query(request: QueryRequest):
    # 1. Forward the query to your fresh 4-bit local model build
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
                function_args = tool_calls[0].get("function", {}).get("arguments", "{}")
                if isinstance(function_args, str):
                    function_args = json.loads(function_args)
                
                target_city = function_args.get("city_name")
                
                if target_city:
                    # 3. Securely execute the external real-time weather lookup
                    live_weather_data = await fetch_imd_weather_data(target_city)
                    return {
                        "status": "success",
                        "city": target_city,
                        "tool_triggered": "fetch_imd_city_forecast",
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
