import pika
import json
import psycopg2
import os
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()


def get_pg_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        dbname=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD")
    )


def get_supabase_client():
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="sensor_data")


conn = get_pg_connection()
cur = conn.cursor()
supabase: Client = get_supabase_client()

def callback(ch, method, properties, body):
    data = json.loads(body)

    for room_data in data["rooms"]:
        room = room_data["room"]
        life = room_data["life_sensor"]
        iaq = room_data["iaq_sensor"]
        power = data["power_meter"]  

        
        cur.execute("""
            INSERT INTO life_sensor_data (timestamp, device_id, online_status, sensitivity, presence_state)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (device_id, timestamp) DO NOTHING
        """, (
            life['timestamp'],
            life['device_id'],
            life['online_status'],
            life['sensitivity'],
            life['presence_state']
        ))

        
        cur.execute("""
            INSERT INTO iaq_sensor_data (timestamp, device_id, co2, temperature, humidity)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (device_id, timestamp) DO NOTHING
        """, (
            iaq['timestamp'],
            iaq['device_id'],
            iaq['co2'],
            iaq['temperature'],
            iaq['humidity']
        ))

        cur.execute("""
            INSERT INTO power_sensor_data (
                timestamp, device_id, 
                power_meter_1, power_meter_2, power_meter_3, 
                power_meter_4, power_meter_5, power_meter_6
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (device_id, timestamp) DO NOTHING
        """, (
            power['timestamp'],
            power['device_id'],
            power['power_meter_1'],
            power['power_meter_2'],
            power['power_meter_3'],
            power['power_meter_4'],
            power['power_meter_5'],
            power['power_meter_6']
        ))


        
        supabase.table("latest_sensor_data").upsert({
            "room": room,
            "timestamp": life["timestamp"],
            "life_data": json.dumps(life),
            "iaq_data": json.dumps(iaq),
            "power_data": json.dumps(power)
        }).execute()

    conn.commit()

channel.basic_consume(queue="sensor_data", on_message_callback=callback, auto_ack=True)
print("✅ Listening for Combined Sensor Data...")
channel.start_consuming()
