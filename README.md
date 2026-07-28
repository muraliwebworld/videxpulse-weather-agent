# Videxpulse Weather Agent

A modern full-stack weather application with ReactJS frontend and FastAPI backend, powered by Ollama for intelligent JSON validation and IMD REST API for real-time weather data.

## Architecture Overview

```
[ReactJS App UI] ──(POST /api/chat)──> [FastAPI Backend] ──> [Ollama (JSON Check)]
       ▲                                      │
       │                               (Triggers Tool)
       │                                      ▼
       └─────────── (Renders Final JSON) <── [IMD REST API Call]
```

### Components

- **Frontend**: ReactJS with Vite for rapid development
- **Backend**: FastAPI with async/await support
- **AI Validation**: Ollama for JSON validation and data integrity checks
- **Data Source**: IMD REST API for weather information

## Prerequisites

- Node.js 16+ (for React frontend)
- Python 3.9+ (for FastAPI backend)
- Ollama installed and running (for JSON validation)
- Internet connection (for IMD API calls)

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
- **Description**: Send weather queries and receive JSON-validated responses
- **Request Body**:
  ```json
  {
    "message": "What's the weather in Mumbai?",
    "location": "Mumbai"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "data": {
      "location": "Mumbai",
      "temperature": 28.5,
      "condition": "Partly Cloudy",
      "humidity": 65,
      "wind_speed": 12
    },
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
OLLAMA_BASE_URL=http://localhost:11434
IMD_API_BASE_URL=https://api.imdpune.gov.in
DEBUG=True
PORT=8000
```

## Integration Points

### Ollama Integration
- Validates JSON responses from IMD API
- Ensures data integrity and consistency
- Provides intelligent error handling

### IMD API Integration
- Fetches real-time weather data
- Supports multiple locations
- Weather forecasting data

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

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
