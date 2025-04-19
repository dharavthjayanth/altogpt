from openai import OpenAI
import os
import json
from backend.utils import get_latest_supabase_data

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def get_ai_response(user_query: str) -> str:
    """
    Takes a user query like "What's the CO2 in room 101?"
    and responds with an intelligent answer using GPT-4.
    """
   
    data = get_latest_supabase_data()

    
    sensor_summary = []
    for room in data:
        room_id = room["room"]
        iaq = room["iaq_data"]
        presence = room["life_data"]["presence_state"]
        co2 = iaq.get("co2", "N/A")
        temp = iaq.get("temperature", "N/A")
        hum = iaq.get("humidity", "N/A")

        sensor_summary.append(
            f"Room {room_id}: Occupancy={presence}, CO2={co2} ppm, Temp={temp} °C, Humidity={hum}%"
        )

    context = "\n".join(sensor_summary)

    prompt = f"""
    You are a smart building assistant. Based on the current live sensor data below, 
    answer the user's question accurately and clearly.

    Sensor Data:
    {context}

    User Question:
    {user_query}

    Response:
    """

 
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an intelligent building IoT assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    answer = completion.choices[0].message.content
    return answer
