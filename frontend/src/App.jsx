import { useState } from 'react';

export default function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [weatherResult, setWeatherResult] = useState(null);
  const [error, setError] = useState('');
    // --- ADD THIS LINE TO FIX THE DEFINITION ERROR ---
  const [rawJson, setRawJson] = useState(''); 

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setWeatherResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: query }),
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        setWeatherResult(data);
        // --- BULLETPROOF FIX: Check both snake_case and camelCase to protect assignments ---
        const agentOutput = data.raw_json || data.rawJson || '';
        setRawJson(agentOutput);
        console.log("🎯 Frontend received agent payload:", agentOutput); // Simple browser log verify        
      } else if (data.status === 'fallback') {
        setError(data.message || 'The model did not trigger a weather tool.');
      } else {
        setError('Failed to fetch structured response from weather agent.');
      }
    } catch (err) {
      setError('Could not connect to the local FastAPI backend server.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans p-6 md:p-12">
      <div className="max-w-5xl mx-auto">
        {/* Header Unit */}
        <header className="mb-10 text-center md:text-left">
          <div className="flex items-center justify-center md:justify-start space-x-3 mb-2">
            <span className="text-3xl">🇮🇳</span>
            <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-orange-400 via-white to-green-400 bg-clip-text text-transparent">
              VidexPulse Weather AI Agent Hub
            </h1>
          </div>
          <p className="text-slate-400 text-sm md:text-base">
            Fine-tuned Qwen 1.5B edge agent dynamically routing requests to official open-mateo endpoints.
          </p>
        </header>

        {/* Input Control Form */}
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl mb-8">
          <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about weather (e.g., Will it rain in Gobi town tomorrow?)"
              className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-orange-500 transition-all text-sm md:text-base"
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-orange-500 hover:bg-orange-600 disabled:bg-slate-700 text-white font-semibold px-6 py-3 rounded-lg shadow-md transition-all flex items-center justify-center space-x-2 min-w-[140px]"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <span>Routing...</span>
                </>
              ) : (
                <span>Ask AI Agent</span>
              )}
            </button>
          </form>
        </div>

        {/* Error Callouts */}
        {error && (
          <div className="bg-red-900/30 border border-red-500 text-red-200 rounded-lg p-4 mb-8 text-sm">
            ⚠️ {error}
          </div>
        )}

        {/* Main Weather Visual Dashboard Panel */}
        {weatherResult && (
          <main className="space-y-6 animate-fadeIn">
            {/* Context Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 flex flex-col justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Target Entity</span>
                <span className="text-2xl font-bold capitalize text-orange-400 mt-2">{weatherResult.city}</span>
              </div>
              <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 flex flex-col justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Triggered Method</span>
                <span className="text-sm font-mono bg-slate-950 px-2 py-1 rounded border border-slate-800 mt-2 text-green-400 break-all">
                  {weatherResult.tool_triggered}()
                </span>
              </div>
              <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 flex flex-col justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Station Status</span>
                <span className="text-sm text-slate-300 mt-2 flex items-center space-x-2">
                  <span className="h-2 w-2 rounded-full bg-green-500 inline-block animate-pulse"></span>
                  <span>Live API Connection Verified</span>
                </span>
              </div>
            </div>

            {/* Live Real-Time Dashboard View */}
            <section className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl">
              <h2 className="text-sm font-bold mb-4 text-slate-400 border-b border-slate-700 pb-2 uppercase tracking-wide">
                Current Observations Profile
              </h2>
              
              {!weatherResult.data || weatherResult.data.error ? (
                <div className="text-slate-400 text-center py-6 text-sm italic">
                  {weatherResult.data?.error || "No active data parameters returned."}
                </div>
              ) : (
                <div className="flex flex-col md:flex-row items-center justify-between gap-6 p-4 bg-slate-950/40 rounded-lg">
                  <div className="flex items-center space-x-4">
                    {weatherResult.data.condition_icon && (
                      <img 
                        src={`https:${weatherResult.data.condition_icon}`} 
                        alt="Weather Condition Icon" 
                        className="w-16 h-16 bg-slate-800 rounded-full p-2 border border-slate-700 shadow"
                      />
                    )}
                    <div>
                      <div className="text-4xl font-black text-slate-100 font-mono tracking-tight">
                        {weatherResult.data.temp_c}°C
                      </div>
                      <div className="text-sm text-slate-400 mt-0.5">
                        Feels like <span className="text-orange-300 font-mono">{weatherResult.data.feelslike_c}°C</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-6 w-full md:w-auto text-center md:text-left border-t md:border-t-0 md:border-l border-slate-800 pt-4 md:pt-0 md:pl-6">
                    <div>
                      <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Sky Condition</span>
                      <span className="text-sm font-semibold text-slate-200">{weatherResult.data.condition_text}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Humidity</span>
                      <span className="text-sm font-semibold text-cyan-400 font-mono">💧 {weatherResult.data.humidity}%</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Wind Speed</span>
                      <span className="text-sm font-semibold text-green-400 font-mono">💨 {weatherResult.data.wind_kph} km/h</span>
                    </div>
                  </div>
                </div>
              )}
            </section>
            {/* --- INTERACTIVE TERMINAL PREVIEW BLOCK --- */}
            {rawJson && (
              <section className="mt-8 bg-slate-950 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
                {/* Terminal Window Header Bar */}
                <div className="bg-slate-900 px-4 py-3 flex items-center justify-between border-b border-slate-800">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                    <span className="text-xs text-slate-500 font-mono pl-2">agent_inference_monitor.sh</span>
                  </div>
                  <span className="text-[10px] font-mono bg-green-500/10 text-green-400 border border-green-500/20 px-2 py-0.5 rounded">
                    OLLAMA STREAM ACTIVE
                  </span>
                </div>
                
                {/* Code Body Workspace */}
                <div className="p-5 font-mono text-sm leading-relaxed overflow-x-auto text-emerald-400 bg-slate-950">
                  <div className="text-slate-500 mb-2">// Structural JSON payload from model:</div>
                  <pre className="whitespace-pre-wrap break-all text-blue-300">
                    {(() => {
                      try {
                        let parsed = typeof rawJson === 'string' ? JSON.parse(rawJson) : rawJson;
                        if (Array.isArray(parsed) && parsed[0]?.function?.arguments && typeof parsed[0].function.arguments === 'string') {
                          parsed[0].function.arguments = JSON.parse(parsed[0].function.arguments);
                        }
                        return JSON.stringify(parsed, null, 2);
                      } catch (e) {
                        return String(rawJson);
                      }
                    })()}
                  </pre>
                </div>
              </section>
            )}            
          </main>
        )}
      </div>
    </div>
  );
}
