# ESP32 og IoT netværk

## ESP32 som access point og webserver

I opgaverne blev ESP32 brugt som:

- WiFi access point
- DHCP-server for klienter
- HTTP webserver
- GPIO controller

Typisk setup:

```text
Telefon/laptop -> WiFi -> ESP32 AP -> HTTP side på port 80
```

HTTP bruger normalt:

```text
TCP port 80
```

Når browseren åbner ESP32-websiden, kan Wireshark vise:

```text
TCP three-way handshake
HTTP GET
HTTP response med HTML
```

TCP handshake:

```text
SYN -> SYN/ACK -> ACK
```

God eksamensforklaring:

ESP32 kan fungere som en lille selvstændig netværksenhed. Når den kører som access point, kan klienter forbinde direkte til den uden normal router. Webserveren sender HTML til klienten, og knapper på websiden kan styre GPIO-pins.

## ESP-NOW

ESP-NOW er direkte trådløs kommunikation mellem ESP32-enheder uden almindeligt WiFi access point.

Typisk setup:

```text
ESP32 sender -> ESP-NOW -> ESP32 receiver
```

Bruges til små datapakker, fx:

- temperatur
- joystick værdi
- potentiometer værdi
- sensorstatus

Vigtige begreber:

- MAC-adresse bruges til at kende peer/enhed
- callback funktion bruges når data sendes/modtages
- struct bruges ofte til at sende flere værdier samlet

Eksempel ide:

```cpp
typedef struct sensor_data {
    int id;
    float value;
} sensor_data;
```

God eksamensforklaring:

ESP-NOW er nyttigt til IoT, fordi enheder kan kommunikere direkte uden router eller broker. MQTT kræver en broker, men ESP-NOW sender direkte mellem ESP32-enheder.

## ESP32 med MQTT

ESP32 kan også være MQTT publisher/subscriber.

Eksempel topic fra opgaverne:

```text
esp32/temp
```

Flow:

```text
ESP32 læser sensor -> publicerer til broker -> telefon/PC subscriber modtager
```

God test:

- Serial monitor viser sensorværdi
- MQTT app subscriber på samme topic
- Wireshark på broker viser `tcp.port == 1883`

