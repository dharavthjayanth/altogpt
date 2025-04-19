import os
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_latest_supabase_data():
    data = supabase.table("latest_sensor_data").select("*").execute()
    parsed = []
    for row in data.data:
        parsed.append({
            "room": row['room'],
            "timestamp": row['timestamp'],
            "life_data": row['life_data'] if isinstance(row['life_data'], dict) else json.loads(row['life_data']),
            "iaq_data": row['iaq_data'] if isinstance(row['iaq_data'], dict) else json.loads(row['iaq_data']),
            "power_data": row['power_data'] if isinstance(row['power_data'], dict) else json.loads(row['power_data'])
        })
    return parsed
