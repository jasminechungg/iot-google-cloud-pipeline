# iot-google-cloud-pipeline
An Edge-to-Cloud IoT solution for smart cold chain monitoring using ESP32, MQTT, Google Pub/Sub, Cloud Run, and Firestore.

# Smart Cold Chain Monitoring System 🚛❄️
### CPC357: IoT Architecture & Smart Applications
**Assignment 2: Design and Development of an IoT Application on Google Cloud Platform**

---

## 📌 Project Overview
This project implements a complete **Edge-to-Cloud IoT pipeline** designed for **Food Supply Chain Logistics**. It monitors the real-time environmental conditions (temperature & humidity) and geospatial location of refrigerated delivery trucks to prevent food spoilage and ensure safety compliance.

The system integrates physical hardware at the edge with a scalable, serverless cloud backend using the **Google Cloud Platform (GCP)**.

### 🌟 Key Features
* **Real-time Monitoring:** Captures temperature, humidity, and GPS location every 5 seconds.
* **Edge-to-Cloud Bridge:** Uses an intermediary **Secure Gateway (VM)** to bridge MQTT traffic to Google Cloud Pub/Sub.
* **Serverless Processing:** Uses **Google Cloud Run** to process data on-demand, reducing costs.
* **Smart Logic:** Automatically flags cargo status as **"HOT"** or **"OK"** based on temperature thresholds.
* **NoSQL Storage:** Stores unstructured telemetry data in **Google Firestore** for historical analysis.

---

## 🚀 System Architecture
The system follows a 3-tier IoT architecture:

1.  **Edge Layer (Device):**
    * **Hardware:** Cytron Maker Feather S3 (ESP32).
    * **Sensors:** DHT11 (Temp/Hum), GPS NEO-6M (Location).
    * **Protocol:** MQTT (Lightweight).
2.  **Gateway Layer (Bridge):**
    * **Host:** Google Compute Engine (VM).
    * **Software:** Eclipse Mosquitto Broker & Python Bridge Script.
    * **Function:** Translates MQTT messages -> Google Pub/Sub events.
3.  **Cloud Layer (Backend):**
    * **Ingestion:** Google Cloud Pub/Sub.
    * **Processing:** Google Cloud Run (Python container).
    * **Storage:** Google Firestore (Native Mode).

---

## 📂 Repository Structure

```text
📦 smart-cold-chain-iot
 ┣ 📂 firmware
 ┃ ┗ 📜 cpc357assg2.ino       # Arduino code for ESP32 (Edge Node)
 ┣ 📂 gateway
 ┃ ┗ 📜 bridge.py             # Python script for VM Gateway (MQTT -> Pub/Sub)
 ┣ 📂 cloud
 ┃ ┣ 📜 main.py               # Cloud Run function logic
 ┃ ┗ 📜 requirements.txt      # Python dependencies for Cloud Run
 ┗ 📜 README.md               # Project documentation
```
## 🛠️ Hardware & Software Requirements
**Hardware**
* Cytron Maker Feather S3 (or any ESP32 board)

* DHT11 Temperature & Humidity Sensor

* GPS NEO-6M Module

* Jumper Wires & Breadboard

**Software & Cloud Services**
* IDE: Arduino IDE (v2.0+)

* Language: C++ (Arduino), Python 3.10+

* Google Cloud Platform:

   * Compute Engine (VM)

   * Pub/Sub

   * Cloud Run (2nd Gen)

   * Firestore

* Gateway: Eclipse Mosquitto MQTT Broker

## ⚙️ Setup & Installation Guide
1. Edge Node Setup (Firmware)
   
  a. Navigate to the firmware/ folder.
  
  b. Open cpc357assg2.ino in Arduino IDE.

  c. Install the following libraries via Library Manager:

    PubSubClient (by Nick O'Leary)

    ArduinoJson (by Benoit Blanchon)

    DHT sensor library (by Adafruit)

  d. Configuration: Update the following lines in the code with your credentials:

```bash
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "YOUR_VM_EXTERNAL_IP";
```

  e. Upload the code to your ESP32 board.

2. Gateway Setup (Virtual Machine)

  a. SSH into your Google Compute Engine VM.

  b. Install Mosquitto Broker:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

  c. Install Python Dependencies:

```bash
pip3 install paho-mqtt google-cloud-pubsub
```

 d. Security Key: 
 
     Download your Service Account Key (JSON) from Google Cloud IAM.
  
    Rename it to key.json.

    Upload it to the same directory as bridge.py.

  e. Run the Bridge:

```bash
python3 bridge.py
```

3. Cloud Backend Deployment
  a. Pub/Sub: Create a topic named sensor-data-topic.

  b. Cloud Run:

    Navigate to the cloud/ folder.

    Deploy the function using the gcloud CLI:

```bash
gcloud run deploy save-to-firestore \
  --source . \
  --function subscribe \
  --region us-central1 \
  --allow-unauthenticated
```
>Note: Ensure the Cloud Run service account has Datastore User permissions.

  c. Eventarc: Create an Eventarc trigger to link the Pub/Sub topic to the Cloud Run service.

## 📊 Usage & Verification
1. Monitor Edge: Open the Arduino Serial Monitor (Baud 115200). You should see:

```text
Connecting to WiFi... Connected!
Sending: {"id":"truck_1", "temp":31.5, ...}
```

2. Monitor Gateway: On the VM, the bridge.py script will output:

```text
Received from ESP32: {...}
-> Sent to Google Cloud: MessageID_12345
```

3. Verify Cloud: Go to the Firestore Console. A new document should appear in the data_logs collection every few seconds with the status "HOT" or "OK".

## 👥 Team Members
Ain Nabihah Binti Mahamad Chah Pari (162321)

Jasmine Binti Mohd Shaiful Adli Chung (164191)

## 📄 License
This project was developed for the CPC357: IoT Architecture & Smart Applications course at Universiti Sains Malaysia (USM).
