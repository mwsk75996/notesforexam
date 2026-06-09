# JSON fra ESP32

Hvis ESP32 sender data videre via MQTT eller HTTP, er JSON praktisk:

```cpp
String payload = "{";
payload += "\"temp\":";
payload += temperature;
payload += ",\"humidity\":";
payload += humidity;
payload += "}";
```

Eksempel:

```json
{"temp":25.8,"humidity":25.0}
```
