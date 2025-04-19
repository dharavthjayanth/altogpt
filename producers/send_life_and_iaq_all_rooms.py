import pandas as pd
import pika
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sensor_data')

rooms = ['room_101', 'room_102', 'room_103']

base_path = "C:/Users/jayan/OneDrive/Desktop/altotech_project/data"

life_data = {room: pd.read_csv(f"{base_path}/{room}_life_sensor.csv") for room in rooms}
iaq_data = {room: pd.read_csv(f"{base_path}/{room}_iaq_sensor.csv") for room in rooms}
power_data = pd.read_csv(f"{base_path}/power_meter_data.csv")


min_len = min([len(life_data[room]) for room in rooms] + [len(iaq_data[room]) for room in rooms] + [len(power_data)])

for i in range(min_len):
    for room in rooms:
        payload = {
            "room": room,
            "timestamp": str(life_data[room].iloc[i]['datetime']),
            "life_data": {
                "device_id": f"{room}_life",
                "online_status": life_data[room].iloc[i]['online_status'],
                "sensitivity": life_data[room].iloc[i]['sensitivity'],
                "presence_state": life_data[room].iloc[i]['presence_state']
            },
            "iaq_data": {
                "device_id": f"{room}_iaq",
                "co2": iaq_data[room].iloc[i]['co2'],
                "temperature": iaq_data[room].iloc[i]['temperature'],
                "humidity": iaq_data[room].iloc[i]['humidity']
            },
            "power_data": {
                "device_id": "power_meter",
                "power_meter_1": power_data.iloc[i]['power_kw_power_meter_1'],
                "power_meter_2": power_data.iloc[i]['power_kw_power_meter_2'],
                "power_meter_3": power_data.iloc[i]['power_kw_power_meter_3'],
                "power_meter_4": power_data.iloc[i]['power_kw_power_meter_4'],
                "power_meter_5": power_data.iloc[i]['power_kw_power_meter_5'],
                "power_meter_6": power_data.iloc[i]['power_kw_power_meter_6']
            }
        }

        print("[SENDING]", payload)
        channel.basic_publish(exchange='', routing_key='sensor_data', body=json.dumps(payload))

    time.sleep(5)

connection.close()
