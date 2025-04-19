# 🏢 AltoTech AI-Powered IoT Platform

Welcome to **AltoGPT** – a generative AI assistant that powers smart building management using real-time sensor data, intelligent insights, and a sleek mobile interface.

---

## 🚀 Features

- Real-time streaming from IAQ, occupancy, and power sensors
- AI-generated summaries, recommendations, and analytics
- Supabase + TimescaleDB integration
- LangChain-powered AI inference pipeline
- Responsive React mobile UI with voice input
- Modular, Dockerized microservices

---

## 📦 Project Structure

```
ALTOTECH_PROJECT/
├── agents/
│   └── agent_router.py
├── backend/
│   ├── backend_inference_main/      # LangChain AI pipeline
│   ├── rag/                         # Retrieval-Augmented Generation
│   ├── tools/                       # Tools like energy calculator
│   ├── utils/                       # Supabase client helpers
│   ├── main.py                      # FastAPI entrypoint
│   ├── requirements.txt
│   └── Dockerfile
├── consumers/
│   └── combined_consumer.py
├── data/                            # Simulated sensor CSVs
├── producers/
│   └── send_combined_to_rabbitmq.py # Publishes combined IAQ, occupancy, power
├── services/
│   ├── send_combined_to_db.py       # TimescaleDB consumer
│   └── send_combined_to_supabase.py # Supabase real-time updater
├── dashboard/                       # (Optional) Streamlit dashboard
├── frontend/                        # React frontend UI
│   ├── src/
│   └── Dockerfile
├── .env
├── docker-compose.yml
├── .dockerignore
└── README.md
```

---

## ⚙️ Environment Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-org/altotech-platform.git
cd altotech-platform
```

### 2. Create a `.env` file with:
```env

PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=altotech
PG_USER=postgres
PG_PASSWORD=shreyasha123


SUPABASE_URL=https://wxwmbikghvdoixopbzmr.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind4d21iaWtnaHZkb2l4b3Biem1yIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NDU2OTc0MiwiZXhwIjoyMDYwMTQ1NzQyfQ.nQ7WmOygKGmc7ecPGa60sU6HUgid6mfUdEuV8yOq6Ns


OPENAI_API_KEY=sk-svcacct-vPTeI5m4lr8Omi8Nl--zFO2Dar97AIqPeW3xQH0zYKh80vP-ET34un9o0Fs8xT3BlbkFJuuj6Waf1AhBJnB9YHqmrbEAaXT3yqNyNtmYdmr7mx7leDOzZ-oQTSt6bhEbAA
```

### 3. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

---

## 🐳 Run Locally with Docker Compose
```bash
docker-compose up --build
```
> This will spin up FastAPI, React, RabbitMQ, and TimescaleDB containers.

---

## 🧪 Testing the System

### 1. Start sensor simulation (RabbitMQ publisher)
```bash
python producers/send_combined_to_rabbitmq.py
```

### 2. Start Supabase updater
```bash
python services/send_combined_to_supabase.py
```

### 3. Start TimescaleDB storage
```bash
python services/send_combined_to_db.py
```

---

## 🌐 Frontend (React UI)
```bash
cd frontend
npm install
npm start
```
Visit: [http://localhost:3000](http://localhost:3000)

---

## 🔍 REST API Endpoints (FastAPI)

| Endpoint                              | Method | Description                                      |
|---------------------------------------|--------|--------------------------------------------------|
| `/`                                   | GET    | Welcome message                                 |
| `/query/`                             | POST   | Ask questions to ALTO-GPT (AI inference)         |
| `/buildings/`                         | GET    | List available buildings                         |
| `/buildings/{building_id}/status/`   | GET    | Current building sensor overview                 |
| `/rooms/{room_id}/sensors/{type}/`   | GET    | Get specific sensor data for a room              |

---

## 🤖 AI Features

- LangChain + GPT-3.5 Turbo powered agent
- Tool calling with sensor summary, power estimation, RAG
- Multi-input tool for direct sensor queries
- Voice input + AI chat interface in frontend
- Summarization with actionable recommendations

---

## 🧪 Testing Instructions

### Local Development

- **Backend**: `uvicorn backend.main:app --reload`
- **Frontend**: `npm start`
- Ensure `.env` is properly configured for PostgreSQL and Supabase

### API Testing Tools

- Use Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Use Postman or curl to test `/query/` and `/buildings/...` routes

---

## 📊 Architecture Diagram

![Architecture](./assets/flowchart.png)

> Includes data ingestion, AI inference, and frontend rendering layers.

---

## 🚀 Deployment

- All services are containerized
- Frontend deployed on Vercel: [[https://your-vercel-link](https://altogpt-jayanths-projects-3b08736b.vercel.app/)](#)
- Backend optionally deployed on Render or run locally
- CI/CD with GitHub Actions workflows: test, build, deploy



