# VidexPulse Weather AI Agent 🌤️

A modern full-stack weather intelligence application with ReactJS frontend and FastAPI backend, powered by a **fine-tuned Qwen AI model** for intelligent weather query understanding and tool-calling, plus real-time weather data integration.

This project uses the **VidexPulse Weather Agent AI Model** - a specialized fine-tuned language model designed to understand natural language weather queries, intelligently call weather data APIs, and generate professional weather reports in markdown format.

## 🎯 Key Features

- **AI-Powered Query Understanding** - Uses fine-tuned Qwen 1.5B model for intelligent weather query recognition
- **Tool-Calling Capability** - Automatically identifies required weather data and calls appropriate tools
- **Professional Report Generation** - Transforms raw weather data into beautifully formatted markdown reports
- **37+ City Coverage** - Supports Tamil Nadu and Indian cities with natural language variations
- **Real-time Weather Data** - Integration with weather APIs for live forecasts
- **Chat Interface** - Modern ReactJS UI for seamless user interaction

## Architecture Overview

```
[ReactJS UI] 
       ▲
       │ (User Query)
       ▼
[FastAPI Backend]
       │
       ├─> [VidexPulse Weather Agent AI Model] (Qwen 1.5B Fine-Tuned)
       │        │
       │        ├─> Tool-Calling Detection
       │        └─> Query Understanding
       │
       ├─> [Weather APIs]
       │        └─> Fetch Real-time Data
       │
       └─> [Response Formatter]
            └─> Markdown Generation
       │
       └──> [Renders Final Report] ──> [User]
```

### Components

- **Frontend**: ReactJS with Vite for rapid development
- **Backend**: FastAPI with async/await support
- **AI Model**: VidexPulse Weather Agent (Qwen 1.5B, 4-bit GGUF, fine-tuned)
- **Inference Engine**: Ollama for efficient model inference
- **Data Source**: Weather APIs for real-time information

## Prerequisites

- **Node.js 16+** (for React frontend)
- **Python 3.9+** (for FastAPI backend)
- **Ollama** (for AI model inference) - [Install from ollama.com](https://ollama.com)
- **Git LFS** (for downloading large model files)
- **Internet connection** (for API calls and model download)

## Project Structure

```
videxpulse-weather-agent/
├── frontend/                 # React UI application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/                  # FastAPI server
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   └── models/
│   ├── requirements.txt
│   └── .env.example
└── docker-compose.yml        # Local development setup
```

## 🤖 AI Model Setup: VidexPulse Weather Agent

The application uses the **VidexPulse Weather Agent** - a specialized fine-tuned AI model available on Hugging Face.

### Model Information

| Property | Value |
|----------|-------|
| **Model Name** | videexpulse-weather-agent |
| **Base Model** | Qwen 1.5B |
| **Quantization** | 4-bit GGUF |
| **Training Datasets** | 98,724+ weather query examples |
| **Task** | Tool-Calling + Response Generation |
| **Hugging Face Link** | [muraliwebworld/videxpulse-weather-agent](https://huggingface.co/muraliwebworld/videxpulse-weather-agent) |

### What This Model Does

The model is trained on two key tasks:

#### 1. **Tool-Calling (Query Understanding)**
Recognizes weather queries and generates structured tool requests to fetch weather data.

**Example Input:**
```
"Will it rain in Coimbatore tomorrow?"
```

**Model Output (Tool Call):**
```json
{
  "id": "call_imd_12345",
  "type": "function",
  "function": {
    "name": "fetch_imd_city_forecast",
    "arguments": "{\"city_name\": \"coimbatore\"}"
  }
}
```

#### 2. **Response Generation (Report Formatting)**
Transforms raw weather data into professional, readable markdown reports.

**Example Input (Raw Data):**
```json
{
  "station": "Coimbatore",
  "district": "Coimbatore",
  "forecast": [{
    "date": "2026-08-06",
    "rainfall_mm": 15.2,
    "condition": "Light Thunderstorms",
    "max_temp": 33.0
  }]
}
```

**Model Output:**
```markdown
### Official Weather Update: Coimbatore

* **Expected Weather:** Light thunderstorms expected on August 6.
* **Rainfall Depth:** Moderate rain measuring **15.2 mm** expected.
* **Temperature:** Maximum daytime highs around 33°C.
```

### Downloading the Model

#### Option 1: Automatic Download via Hugging Face Hub

```bash
# Install Hugging Face CLI
pip install huggingface-hub

# Download the model
huggingface-cli download muraliwebworld/videxpulse-weather-agent \
  --local-dir ./models/weather-agent
```

#### Option 2: Using Git LFS

```bash
# Install Git LFS
brew install git-lfs
git lfs install

# Clone the model repository
git clone https://huggingface.co/muraliwebworld/videxpulse-weather-agent
cd videxpulse-weather-agent
```

#### Option 3: Direct Download

Visit [https://huggingface.co/muraliwebworld/videxpulse-weather-agent](https://huggingface.co/muraliwebworld/videxpulse-weather-agent) and download the files manually.

### Setting Up Ollama with the Model

1. **Download the model** (using one of the methods above)

2. **Create a Modelfile** in your project directory:

```dockerfile
FROM ./videxpulse-weather-agent.gguf

# Inference parameters for focused, deterministic outputs
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"

# ChatML template for proper message formatting
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>
"""

# System prompt for weather agent behavior
SYSTEM """You are an official VidexPulse Weather Agent. If a user asks about the weather, you must call the 'fetch_imd_city_forecast' tool with the exact city name in JSON format."""
```

3. **Create the Ollama model:**

```bash
ollama create videxpulse-weather-agent -f Modelfile
```

4. **Test the model:**

```bash
ollama run videxpulse-weather-agent "What's the weather in Chennai tomorrow?"
```

### Supported cities

Supports all major cities around the world

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Run the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```

### AI Model Setup

Before running the application, you need to set up the VidexPulse Weather Agent model:

1. **Install Ollama** (if not already installed):
   - Visit [ollama.com](https://ollama.com) and download for your OS
   - Verify installation:
   ```bash
   ollama --version
   ```

2. **Download the Weather AI Model**:
   ```bash
   # Method 1: Using Hugging Face CLI (Recommended)
   pip install huggingface-hub
   huggingface-cli download muraliwebworld/videxpulse-weather-agent \
     --local-dir ./models/weather-agent
   
   # OR Method 2: Using Git LFS
   brew install git-lfs && git lfs install
   git clone https://huggingface.co/muraliwebworld/videxpulse-weather-agent ./models/weather-agent
   ```

3. **Create Ollama Model**:
   
   In the project root, create `Modelfile`:
   ```dockerfile
   FROM ./models/weather-agent/videxpulse-weather-agent.gguf

   PARAMETER temperature 0.1
   PARAMETER top_p 0.9
   PARAMETER stop "<|im_start|>"
   PARAMETER stop "<|im_end|>"

   TEMPLATE """{{ if .System }}<|im_start|>system
   {{ .System }}<|im_end|>
   {{ end }}{{ if .Prompt }}<|im_start|>user
   {{ .Prompt }}<|im_end|>
   {{ end }}<|im_start|>assistant
   {{ .Response }}<|im_end|>
   """

   SYSTEM """You are an official VidexPulse Weather Agent. If a user asks about the weather, you must call the 'fetch_imd_city_forecast' tool with the exact city name in JSON format."""
   ```

   Then create the model:
   ```bash
   ollama create videxpulse-weather-agent -f Modelfile
   ```

4. **Start Ollama Service**:
   ```bash
   # In a separate terminal
   ollama serve
   ```

5. **Test the Model**:
   ```bash
   ollama run videxpulse-weather-agent "What's the weather in Coimbatore?"
   ```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Chat Endpoint
- **POST** `/api/chat`
- **Description**: Send weather queries and receive AI-processed responses with real-time data
- **Request Body**:
  ```json
  {
    "message": "What's the weather in Chennai tomorrow?",
    "location": "Chennai"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "data": {
      "location": "Chennai",
      "forecast": {
        "date": "2026-08-07",
        "condition": "Partly Cloudy",
        "temperature": 28.5,
        "max_temp": 32.0,
        "min_temp": 25.0,
        "humidity": 65,
        "wind_speed": 12,
        "rainfall_mm": 0.0
      },
      "report": "### Official Weather Update: Chennai\n\n* **Expected Weather:** Partly cloudy skies throughout the day.\n* **Temperature:** Highs around 32°C, lows around 25°C.\n* **Humidity:** 65% - comfortable levels.\n* **Wind:** Light breeze at 12 km/h."
    },
    "tool_called": "fetch_imd_city_forecast",
    "validated": true
  }
  ```

## Development

### Running Both Services

For development, run both services in separate terminals:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Environment Variables

Backend `.env.example`:
```
# Ollama Configuration (for AI Model Inference)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=videxpulse-weather-agent

# Weather API Configuration
WEATHER_API_BASE_URL=https://api.weather.example.com
WEATHER_API_KEY=your_api_key_here

# Application Settings
DEBUG=True
PORT=8000
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Integration Points

### VidexPulse Weather Agent AI Model Integration
- Understands natural language weather queries
- Generates structured tool-calls for data fetching
- Handles multiple city name variations (e.g., "Gobi town" → "gobichettipalayam")
- Transforms raw weather data into professional markdown reports
- Optimized for 37+ Indian cities with cultural variations

### Weather API Integration
- Fetches real-time weather data
- Supports multiple city locations
- Provides forecast data with temperature, rainfall, humidity, wind speed
- Handles location normalization and error cases

### Model Inference with Ollama
- Runs the fine-tuned Qwen 1.5B model efficiently
- Low-latency inference with 4-bit quantization
- Supports GPU acceleration when available
- Provides consistent, reproducible outputs

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## Docker Support

Build and run with Docker Compose:
```bash
docker-compose up -d
```

This will start both frontend and backend services with proper networking.

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 🌟 Usage Examples

### Example 1: Check Tomorrow's Weather

**Input:**
```
"What will be the weather in Salem tomorrow?"
```

**AI Model Process:**
1. Recognizes weather query with city name "Salem"
2. Generates tool call: `fetch_imd_city_forecast(city_name="salem")`
3. API returns forecast data
4. Generates markdown report

**Output:**
```markdown
### Official Weather Update: Salem

* **Date:** August 7, 2026
* **Expected Weather:** Mostly sunny with occasional clouds
* **Temperature Range:** High of 36°C, Low of 26°C
* **Humidity:** 58%
* **Wind Speed:** 15 km/h
```

---

### Example 2: Rain Prediction Query

**Input:**
```
"Will it pour down in Gobi town next week?"
```

**AI Model Process:**
1. Recognizes colloquial city name variation "Gobi town"
2. Maps to canonical name: "gobichettipalayam"
3. Fetches weekly forecast
4. Analyzes rainfall data
5. Generates professional report

**Output:**
```markdown
### Official Weather Update: Gobichettipalayam

* **Week Outlook:** Mixed precipitation expected
* **Rainfall Forecast:** 45-60mm expected across the week
* **Best Days:** Tuesday & Thursday show highest rain probability
* **Recommendation:** Keep umbrella handy; plan outdoor activities accordingly
```

---

### Example 3: Multi-Parameter Weather Query

**Input:**
```
"What are maximum and minimum temperatures for Chennai today?"
```

**AI Model Process:**
1. Extracts specific weather parameters
2. Calls weather API for Chennai
3. Processes temperature data
4. Formats response with emphasis on temperature

**Output:**
```markdown
### Official Weather Update: Chennai

* **Date:** August 6, 2026
* **Maximum Temperature:** 32°C
* **Minimum Temperature:** 25°C
* **Temperature Range:** 7°C variation
* **Heat Index:** Feels like 35°C (due to humidity)
* **Recommendation:** Stay hydrated; avoid peak sun hours (11 AM - 4 PM)
```

## Model Training Details

The VidexPulse Weather Agent model was fine-tuned using:

| Aspect | Details |
|--------|---------|
| **Base Model** | Qwen 1.5B (Chat Version) |
| **Training Data** | 98,724+ weather query examples |
| **Training Method** | Supervised Fine-tuning (SFT) |
| **Quantization** | 4-bit GGUF for efficiency |
| **Training Framework** | RunPod Fine-Tuning Pipeline |
| **Supported Languages** | English + Natural language variations |
| **Inference Speed** | ~100-200ms per query (CPU), <50ms (GPU) |

### Training Datasets

1. **dataset_tool_calling.jsonl** (98,724 examples)
   - Teaches model to recognize weather queries
   - Generates proper tool-calling requests
   - Handles city name variations

2. **dataset_response_generation.jsonl** (50,000+ examples)
   - Teaches model to format raw data as reports
   - Professional markdown generation
   - Data transformation and presentation

## License

MIT License

## 📞 Support & Resources

- **Model Hub:** [Hugging Face - VidexPulse Weather Agent](https://huggingface.co/muraliwebworld/videxpulse-weather-agent)
- **Ollama Docs:** [ollama.com](https://ollama.com)
- **FastAPI Docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **React Docs:** [react.dev](https://react.dev)

## 🚀 Next Steps

1. ✅ Clone the repository
2. ✅ Download the AI model from Hugging Face
3. ✅ Set up Ollama with VidexPulse Weather Agent
4. ✅ Configure backend environment variables
5. ✅ Install frontend dependencies
6. ✅ Run both backend and frontend
7. ✅ Start making weather queries!

---

**Built with ❤️ for weather intelligence**

## Support

For issues and questions, please create an issue in the repository.
