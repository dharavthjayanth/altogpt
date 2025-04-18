import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import { askAI, getBuildingStatus } from './api/index';

function App() {
  const [status, setStatus] = useState(null);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [chat, setChat] = useState([
    { type: 'ai', text: "💬 Hi! I'm ALTO-GPT. How can I assist you today?" }
  ]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat]);

  const handleGetStatus = async () => {
    try {
      const data = await getBuildingStatus();
      setStatus(data);
    } catch (error) {
      console.error('Error fetching building status:', error);
    }
  };

  const handleAskAI = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setChat(prev => [...prev, { type: 'user', text: query }]);

    try {
      const res = await askAI(query);
      setResponse(res);
      setChat(prev => [...prev, { type: 'ai', text: res }, { type: 'recommendation', text: generateRecommendation(res) }]);
    } catch (error) {
      const fallback = '⚠️ Failed to get AI response.';
      setResponse(fallback);
      setChat(prev => [...prev, { type: 'ai', text: fallback }]);
      console.error(error);
    }

    setQuery('');
    setLoading(false);
  };

  const generateRecommendation = (text) => {
    if (text.includes('CO2') || text.includes('co2')) return '🌀 Recommendation: Consider improving ventilation or increasing airflow.';
    if (text.includes('temperature')) return '🌬️ Recommendation: Adjust air conditioning to maintain thermal comfort.';
    if (text.includes('humidity')) return '💧 Recommendation: Use dehumidifiers or HVAC control if needed.';
    if (text.includes('power')) return '⚡ Recommendation: Reduce power usage by optimizing HVAC or lighting.';
    return '📌 Tip: Monitor sensor trends to optimize efficiency and comfort.';
  };

  const handleVoiceInput = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.start();
    recognition.onresult = (event) => {
      const speech = event.results[0][0].transcript;
      setQuery(speech);
    };
  };

  return (
    <div className="container">
      <h1 className="title">🤖 ALTO-GPT</h1>

      <div className="button-group">
        <button onClick={handleGetStatus}>🔍 Check Current Building Status</button>
      </div>

      {status && (
        <div className="status-section">
          <h3>🌡️ Building Averages:</h3>
          <div className="sensor-grid">
            <div className="sensor-box">
              <h4>💨 CO₂</h4>
              <div className="circular-meter" style={{ '--value': status.avg_co2 / 20 }}><span>{status.avg_co2} ppm</span></div>
            </div>
            <div className="sensor-box">
              <h4>🌡️ Temp</h4>
              <div className="circular-meter" style={{ '--value': status.avg_temperature * 2 }}><span>{status.avg_temperature} °C</span></div>
            </div>
            <div className="sensor-box">
              <h4>💧 Humidity</h4>
              <div className="circular-meter" style={{ '--value': status.avg_humidity }}><span>{status.avg_humidity} %</span></div>
            </div>
            <div className="sensor-box">
              <h4>⚡ Power</h4>
              <div className="circular-meter" style={{ '--value': status.total_power_kw / 2 }}><span>{status.total_power_kw} kW</span></div>
            </div>
          </div>

          <h3>📋 Room Details:</h3>
          <div className="sensor-grid">
            {status.rooms.map((room) => (
              <div className="sensor-box" key={room.room}>
                <h4>🚪 {room.room.toUpperCase()}</h4>
                <p className="co2">💨 CO₂: {room.co2} ppm</p>
                <p className="temperature">🌡️ Temp: {room.temperature} °C</p>
                <p className="humidity">💧 Humidity: {room.humidity} %</p>
                <p>👥 Occupancy: {room.occupancy}</p>
                <p>⚡ Power: {room.power_kw} kW</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="query-box">
        <h2>🧠 Ask the Building AI</h2>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder='e.g., "What’s the CO₂ in room 102?"'
        />
        <div className="button-group">
          <button onClick={handleAskAI} disabled={loading}>
            {loading ? 'Thinking...' : 'Ask AI 🤖'}
          </button>
          <button onClick={handleVoiceInput}>🎙️ Speak</button>
        </div>

        <div className="chat-thread">
          {chat.map((msg, idx) => (
            <div key={idx} className={msg.type}>{msg.text}</div>
          ))}
          <div ref={bottomRef} />
        </div>
      </div>
    </div>
  );
}

export default App;
