# ESP32 MQTT sensor pattern

Fra `ass62network`:

```cpp
```

Typisk flow:

```text
1. Start Serial
2. Start sensor library
3. Connect WiFi
4. Sæt MQTT broker med mqttClient.setServer(...)
5. Reconnect WiFi/MQTT i loop()
6. Læs sensor
7. Publish payload til topic
```

Eksempel på topic:

```cpp
const char* MQTT_TOPIC_TEMP = "esp32/temp";
```

Vigtige fejlpunkter:

- WiFi credentials skal passe.
- Broker IP skal være korrekt.
- ESP32 og broker skal kunne nå hinanden på netværket.
- MQTT client ID bør være unik, fx ved at bruge ESP32 MAC.
- DS18B20 kan returnere `-127` hvis sensoren ikke findes eller er koblet forkert.
