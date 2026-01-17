#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>


// --- CONFIGURATION ---
const char* ssid = "iPhone";        // <--- REPLACE
const char* password = "meow";    // <--- REPLACE
const char* mqtt_server = "34.123.184.50";   // <--- REPLACE WITH VM EXTERNAL IP


#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);


WiFiClient espClient;
PubSubClient client(espClient);


void setup() {
  Serial.begin(115200);
  dht.begin();
 
  // 1. Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");


  // 2. Setup MQTT
  client.setServer(mqtt_server, 1883);
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to VM MQTT...");
    // Attempt to connect with a unique ID
    if (client.connect("ESP32_Truck_1")) {
      Serial.println("Connected!");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();


  // 3. Read Data
  float temp = dht.readTemperature();
  // Fake GPS logic (since we are indoors usually)
  float lat = 5.35 + (random(0,100)/10000.0);
  float lng = 100.30 + (random(0,100)/10000.0);


  // 4. Create JSON
  String payload = "{\"id\":\"truck_1\", \"temp\":";
  payload += String(temp);
  payload += ", \"lat\":";
  payload += String(lat, 6);
  payload += ", \"lng\":";
  payload += String(lng, 6);
  payload += "}";


  // 5. Send
  Serial.println("Sending: " + payload);
  client.publish("iot/sensor", payload.c_str());


  delay(5000); // Wait 5 seconds
}
