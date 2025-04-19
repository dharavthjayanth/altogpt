import pandas as pd
import pika
import json
import os
import time

rooms = ['room_101', 'room_102', 'room_103']


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sensor_data')


data = {}
for room in rooms:
    life_file = f"data/{room}_life_sensor.csv"
    iaq_file = f"data/{room}_iaq_sensor.csv"
    data[room] = {
        "life": pd.read_csv(life_file),
        "iaq": pd.read_csv(iaq_file)
    }

power_data = pd.read_csv("data/power_meter_data.csv")

max_rows = max(len(df) for room_data in data.values() for df in room_data.values())
max_rows = max(max_rows, len(power_data))

for i in range(max_rows):
    combined_payload = []

    for room in rooms:
        life_row = data[room]["life"].iloc[i % len(data[room]["life"])]
        iaq_row = data[room]["iaq"].iloc[i % len(data[room]["iaq"])]

        room_data = {
            "room": room,
            "life_sensor": {
                "device_id": f"{room}_life",
                "timestamp": str(life_row['datetime']),
                "online_status": life_row['online_status'],
                "sensitivity": life_row['sensitivity'],
                "presence_state": life_row['presence_state']
            },
            "iaq_sensor": {
                "device_id": f"{room}_iaq",
                "timestamp": str(iaq_row['datetime']),
                "co2": iaq_row['co2'],
                "temperature": iaq_row['temperature'],
                "humidity": iaq_row['humidity']
            }
        }

        combined_payload.append(room_data)

    power_row = power_data.iloc[i % len(power_data)]
    power_meter = {
        "device_id": "power_meter",
        "timestamp": str(power_row['datetime']),
        "power_meter_1": power_row['power_kw_power_meter_1'],
        "power_meter_2": power_row['power_kw_power_meter_2'],
        "power_meter_3": power_row['power_kw_power_meter_3'],
        "power_meter_4": power_row['power_kw_power_meter_4'],
        "power_meter_5": power_row['power_kw_power_meter_5'],
        "power_meter_6": power_row['power_kw_power_meter_6']
    }

    final_payload = {
        "rooms": combined_payload,
        "power_meter": power_meter
    }

    print("[COMBINED PAYLOAD] ", json.dumps(final_payload, indent=2))

    channel.basic_publish(
        exchange='',
        routing_key='sensor_data',
        body=json.dumps(final_payload)
    )

    time.sleep(5)

connection.close()
