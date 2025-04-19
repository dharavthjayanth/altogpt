

import os
import openai
from dotenv import load_dotenv
from backend.utils.supabase_client import get_latest_supabase_data
from backend.tools.energy_calculator import calculate_energy_cost
from backend.rag.retriever import retrieve_context_chunks  

from langchain_community.tools import tool  

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

COST_PER_KWH = 5.5  

@tool
def get_room_status_tool(room_id: str) -> str:
    """Get real-time occupancy and sensor data for a specific room."""
    data = get_latest_supabase_data()
    for entry in data:
        if entry["room"] == room_id:
            iaq = entry["iaq_data"]
            life = entry["life_data"]
            return f"{room_id} → CO2: {iaq['co2']} ppm, Temp: {iaq['temperature']}°C, Humidity: {iaq['humidity']}%, Occupancy: {life['presence_state']}"
    return "No data available for this room."

@tool
def calculate_power_bill_tool(room_id: str, hours: float) -> str:
    """Estimate energy cost for a given room over a period of hours."""
    data = get_latest_supabase_data()
    for entry in data:
        if entry["room"] == room_id:
            power = entry["power_data"]
            if room_id == "room_101":
                usage = power["power_meter_1"] + power["power_meter_2"]
            elif room_id == "room_102":
                usage = power["power_meter_3"] + power["power_meter_4"]
            else:
                usage = power["power_meter_5"] + power["power_meter_6"]
            return calculate_energy_cost(room=room_id, power_kw=usage, hours=hours)
    return "No power data found for the room."

@tool
def retrieve_rag_knowledge_tool(query: str) -> str:
    """Retrieve building manual context chunks relevant to the query."""
    chunks = retrieve_context_chunks(query)
    return "\n".join(chunks)


def ai_query_handler(user_query: str) -> dict:
    try:
        prompt = f"""You are an AI assistant for a smart building. A user asked: \"{user_query}\". 
Respond concisely and accurately based on real-time building sensor context. If data isn't available, say so."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are an expert in building automation and energy monitoring."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.4,
        )

        answer = response.choices[0].message["content"]
        return {"answer": answer.strip()}

    except Exception as e:
        return {"error": str(e)}
