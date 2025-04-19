import pika
import json
import os
import time
from backend.utils.supabase_client import supabase

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sensor_data')

def callback(ch, method, properties, body):
    data = json.loads(body)

    power_data = data.get('power_meter', {})
    rooms_data = data.get('rooms', [])

    for room_entry in rooms_data:
        room = room_entry.get('room')
        timestamp = room_entry['life_sensor'].get('timestamp')

        payload = {
            "room": room,
            "timestamp": timestamp,
            "life_data": room_entry.get('life_sensor', {}),
            "iaq_data": room_entry.get('iaq_sensor', {}),
            "power_data": power_data
        }

        supabase.table('latest_sensor_data').upsert(payload).execute()

    print(f"[SUPABASE] Synced data for Rooms: {[r['room'] for r in rooms_data]}")


channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)

print("Listening for Combined Sensor Data to Supabase...")
channel.start_consuming()
