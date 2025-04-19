from typing import Optional
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain_core.tools import tool
from pydantic import BaseModel
from backend.utils.supabase_client import get_latest_supabase_data
from backend.tools.energy_calculator import calculate_energy_cost
from backend.rag.retriever import retrieve_context_chunks


class DummyInput(BaseModel):
    input: Optional[str] = "N/A"

class QuestionInput(BaseModel):
    query: str

class SensorQueryInput(BaseModel):
    room_id: str
    sensor_type: str  


@tool(args_schema=DummyInput)
def summarize_sensors(input: Optional[str] = None) -> str:
    """Summarize real-time sensor data (CO2, Temp, Humidity, Occupancy) for all rooms."""
    data = get_latest_supabase_data()
    summaries = []
    for entry in data:
        room = entry['room']
        co2 = entry['iaq_data']['co2']
        temp = entry['iaq_data']['temperature']
        humidity = entry['iaq_data']['humidity']
        occ = entry['life_data']['presence_state']
        summaries.append(f"{room}: CO2={co2}, Temp={temp}°C, Humidity={humidity}%, Occupancy={occ}")
    return "\n".join(summaries)


@tool(args_schema=DummyInput)
def compute_power_usage(input: Optional[str] = None) -> str:
    """Estimate current power usage and energy cost for all rooms."""
    data = get_latest_supabase_data()
    total_cost = 0
    summary = []
    for entry in data:
        room = entry['room']
        if room == "room_101":
            power = entry['power_data']['power_meter_1'] + entry['power_data']['power_meter_2']
        elif room == "room_102":
            power = entry['power_data']['power_meter_3'] + entry['power_data']['power_meter_4']
        else:
            power = entry['power_data']['power_meter_5'] + entry['power_data']['power_meter_6']
        cost = calculate_energy_cost(room=room, power_kw=power, hours=1)
        total_cost += power * 5.5
        summary.append(f"{room}: {power:.2f} kW - {cost}")
    return "\n".join(summary + [f"Total Estimated Cost: ฿{total_cost:.2f}"])


@tool(args_schema=QuestionInput)
def fetch_manual_context(query: str) -> str:
    """Retrieve relevant information from building manuals."""
    chunks = retrieve_context_chunks(query)
    return "\n".join(chunks)


@tool
def get_specific_sensor_value(query: str) -> str:
    """Query a specific sensor (e.g., 'temperature in room_101')."""
    try:
        
        parts = query.lower().split(" in ")
        if len(parts) != 2:
            return "Invalid format. Please ask like: 'temperature in room_101'."
        
        sensor_type, room_id = parts
        data = get_latest_supabase_data()
        
        for entry in data:
            if entry["room"] == room_id:
                if sensor_type == "occupancy":
                    return f"Occupancy in {room_id} is {entry['life_data']['presence_state']}."
                elif sensor_type == "power":
                    power = entry["power_data"]
                    usage = (
                        power["power_meter_1"] + power["power_meter_2"]
                        if room_id == "room_101"
                        else power["power_meter_3"] + power["power_meter_4"]
                        if room_id == "room_102"
                        else power["power_meter_5"] + power["power_meter_6"]
                    )
                    return f"Power usage in {room_id} is {usage:.2f} kW."
                else:
                    value = entry["iaq_data"].get(sensor_type)
                    if value is not None:
                        return f"{sensor_type.capitalize()} in {room_id} is {value}."
                    else:
                        return f"{sensor_type} data not found in {room_id}."
        return f"No data found for {room_id}."
    except Exception as e:
        return f"Error: {str(e)}"


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

tools = [
    summarize_sensors,
    compute_power_usage,
    fetch_manual_context,
    get_specific_sensor_value
]

rag_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True  
)

def run_multi_agent_query(query: str) -> str:
    return rag_agent.run(query)
