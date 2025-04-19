import pika
import json



def consume_sensor_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sensor_data')

    def callback(ch, method, properties, body):
        data = json.loads(body)

        print("\n====================== NEW DATA RECEIVED ======================")
        
        # Loop through rooms data
        for room, sensors in data.items():
            if room == "power_meter":
                print(f"[POWER METER DATA] => {sensors}")
            else:
                print(f"[{room.upper()} - LIFE SENSOR] => {sensors['life_sensor']}")
                print(f"[{room.upper()} - IAQ SENSOR] => {sensors['iaq_sensor']}")
        
        print("===============================================================\n")

    channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)
    print("Listening to Sensor Data...")
    channel.start_consuming()



consume_sensor_data()
