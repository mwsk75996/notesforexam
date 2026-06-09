# ESP32 WiFi & MQTT (PubSubClient) med JSON

Komplet skabelon til at forbinde til eksamens-brokeren, modtage/sende data og sende JSON payloads.

```cpp

const char* ssid = "DitWiFiNavn";
const char* password = "DitWiFiKodeord";
const char* mqtt_server = "192.168.1.100"; // Broker IP fra eksamensnetværk

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Forbinder til ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi forbundet! IP: ");
    Serial.println(WiFi.localIP());
}

void reconnect() {
    // Kør i loop indtil vi er forbundet til brokeren
    while (!client.connected()) {
        Serial.print("Forsøger MQTT forbindelse...");
        // Opret unikt klient ID vha. MAC-adresse
        String clientId = "ESP32Client-";
        clientId += String(random(0xffff), HEX);
        
        if (client.connect(clientId.c_str())) {
            Serial.println("forbundet til broker!");
            // Tilmeld topics her hvis der skal lyttes
            client.subscribe("esp32/commands");
        } else {
            Serial.print("fejlede, rc=");
            Serial.print(client.state());
            Serial.println(" prøver igen om 5 sekunder");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop(); // Lad MQTT-klienten arbejde internt

    unsigned long now = millis();
    if (now - lastMsg > 5000) { // Send data hvert 5. sekund
        lastMsg = now;

        int tempValue = 24; // Eksempel: DS18B20 måling
        int gasValue = analogRead(33);

        // Opret JSON payload manuelt
        String payload = "{";
        payload += "\"temp\":";
        payload += tempValue;
        payload += ",\"gas\":";
        payload += gasValue;
        payload += ",\"device_id\":\"ESP32_STATION_1\"";
        payload += "}";

        Serial.print("Publishing: ");
        Serial.println(payload);
        client.publish("esp32/sensor_data", payload.c_str());
    }
}
```

---
