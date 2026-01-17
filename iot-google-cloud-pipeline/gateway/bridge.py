import time
import os
import json
from google.cloud import pubsub_v1
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
# 1. Google Cloud Settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
project_id = "cpc357-481611"  # <--- REPLACE WITH YOUR PROJECT ID
topic_id = "sensor-data-topic"  # The topic you created earlier

# 2. MQTT Settings (Internal)
MQTT_BROKER = "localhost"
MQTT_TOPIC = "iot/sensor"

# --- SETUP PUBSUB PUBLISHER ---
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_to_google(data_str):
    """Takes data from MQTT and pushes it to Google Cloud"""
    try:
        data = data_str.encode("utf-8")
        future = publisher.publish(topic_path, data)
        print(f"-> Sent to Google Cloud: {future.result()}")
    except Exception as e:
        print(f"ERROR: {e}")

# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc):
    print("Bridge Connected to Local MQTT Broker!")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received from ESP32: {payload}")
    # Forward to Google Cloud
    publish_to_google(payload)

# --- MAIN LOOP ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Starting IoT Bridge...")
client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()