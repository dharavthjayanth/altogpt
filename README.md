# 🏢 AltoTech – AI-Powered IoT Platform (AltoGPT)

Welcome to AltoTech's Smart Building AI System – a prototype of **AltoGPT**, your virtual chief engineer. This platform combines real-time IoT data, AI inference, and a mobile-first interface to optimize building sustainability and performance.

---

## 🚀 Features

✅ Real-time IAQ, occupancy, and power monitoring  
✅ AI-powered assistant for contextual building insights  
✅ Voice-enabled chat interface (mobile-first)  
✅ Energy cost estimator and ventilation recommender  
✅ Supabase + TimescaleDB + RabbitMQ + FastAPI backend  
✅ React-based dynamic UI  
✅ Dockerized & CI/CD ready via GitHub Actions  

---

## 📦 Project Structure

ALTOTECH_PROJECT/ 
├── backend/ ← FastAPI backend 
│ ├── main.py 
│ ├── backend_inference_main/ 
│ ├── utils/ 
│ ├── rag/ 
│ └── tools/ 
├── producers/ ← Sensor simulators (Python) 
│ └── send_combined_to_rabbitmq.py 
├── services/ ← AI tools & orchestration 
│ └── ai_inference.py 
├── consumers/ ← RabbitMQ → DB updaters 
│ └── combined_consumer.py 
├── frontend/ ← React mobile-first UI 
│ ├── src/ 
│ ├── public/ 
│ └── App.js 
├── .env ← Environment variables 
├── docker-compose.yml ← Multi-service orchestration 
├── Dockerfile ← Backend container 
├── requirements.txt ← Python dependencies 
├── package.json ← React dependencies └── README.md
