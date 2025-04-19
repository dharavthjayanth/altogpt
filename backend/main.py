from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.backend_inference_main.agent_graph import run_multi_agent_query
from backend.utils.supabase_client import get_latest_supabase_data

app = FastAPI(title="AltoTech AI Inference API")



# ✅ Replace with your actual Vercel frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["."],  # Allow everything for testing (replace in prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to AltoTech AI API"}


class QueryInput(BaseModel):
    query: str

@app.post("/query/", tags=["AI Inference"])
def query_ai(input_data: QueryInput):
    try:
        response = run_multi_agent_query(input_data.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Inference failed: {str(e)}")


@app.get("/buildings/", tags=["Building Info"])
def get_buildings():
    return {
        "buildings": [
            {
                "id": "building_1",
                "name": "AltoTech Main Facility",
                "location": "Bangkok, Thailand"
            }
        ]
    }


@app.get("/buildings/{building_id}/status/", tags=["Building Info"])
def get_building_status(building_id: str):
    if building_id != "building_1":
        raise HTTPException(status_code=404, detail="Building not found")

    latest_data = get_latest_supabase_data()
    if not latest_data:
        raise HTTPException(status_code=404, detail="No live data available")

    rooms_summary = []
    total_power = total_co2 = total_temp = total_humidity = 0

    for entry in latest_data:
        room = entry["room"]
        life = entry["life_data"]
        iaq = entry["iaq_data"]
        power = entry["power_data"]

        room_power = sum([
            power.get("power_meter_1", 0),
            power.get("power_meter_2", 0)
        ]) if room == "room_101" else sum([
            power.get("power_meter_3", 0),
            power.get("power_meter_4", 0)
        ]) if room == "room_102" else sum([
            power.get("power_meter_5", 0),
            power.get("power_meter_6", 0)
        ])

        rooms_summary.append({
            "room": room,
            "occupancy": life["presence_state"],
            "co2": iaq["co2"],
            "temperature": iaq["temperature"],
            "humidity": iaq["humidity"],
            "power_kw": round(room_power, 2)
        })

        total_power += room_power
        total_co2 += iaq["co2"]
        total_temp += iaq["temperature"]
        total_humidity += iaq["humidity"]

    avg = lambda x: round(x / len(latest_data), 2)

    return {
        "building_id": building_id,
        "status": {
            "avg_co2": avg(total_co2),
            "avg_temperature": avg(total_temp),
            "avg_humidity": avg(total_humidity),
            "total_power_kw": round(total_power, 2),
            "rooms": rooms_summary
        }
    }


@app.get("/rooms/{room_id}/sensors/{sensor_type}/", tags=["Room Sensors"])
def get_sensor_value(room_id: str, sensor_type: str):
    valid_sensors = ["co2", "temperature", "humidity", "occupancy", "power"]
    if sensor_type not in valid_sensors:
        raise HTTPException(status_code=400, detail=f"Invalid sensor type. Choose from: {valid_sensors}")

    latest_data = get_latest_supabase_data()
    room_data = next((item for item in latest_data if item["room"] == room_id), None)
    if not room_data:
        raise HTTPException(status_code=404, detail=f"No data found for room: {room_id}")

    if sensor_type == "occupancy":
        value = room_data["life_data"]["presence_state"]
    elif sensor_type == "power":
        power = room_data["power_data"]
        value = sum([
            power.get("power_meter_1", 0),
            power.get("power_meter_2", 0)
        ]) if room_id == "room_101" else sum([
            power.get("power_meter_3", 0),
            power.get("power_meter_4", 0)
        ]) if room_id == "room_102" else sum([
            power.get("power_meter_5", 0),
            power.get("power_meter_6", 0)
        ])
    else:
        value = room_data["iaq_data"].get(sensor_type)

    return {
        "room": room_id,
        "sensor": sensor_type,
        "value": value
    }
