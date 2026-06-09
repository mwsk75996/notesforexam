# MQTT (Message Queuing Telemetry Transport)

MQTT er en letvægts applikationslagsprotokol, der er yderst velegnet til IoT-enheder (som f.eks. ESP32), da den bruger minimal båndbredde og strøm. Den kører typisk over TCP.

## Konceptuelle Roller

MQTT er baseret på en **Publish/Subscribe**-model:

*   **Broker**: Den centrale server, der modtager alle beskeder, filtrerer dem og sender dem videre til interesserede modtagere.
*   **Publisher**: En enhed (f.eks. en ESP32-sensor), der sender (publicerer) en besked til et bestemt emne (topic).
*   **Subscriber**: En enhed (f.eks. en PC eller mobil-app), der tilmelder sig (subscriber på) et bestemt emne for at modtage beskeder.
*   **Topic**: En hierarkisk sti, der fungerer som en kanal (f.eks. `esp32/stue/temperatur`).
*   **Payload**: Selve beskedens indhold (f.eks. `"23.5"`).

### Standard Porte:
*   `1883 TCP` - Ukrypteret standard MQTT-kommunikation.
*   `8883 TCP` - Krypteret MQTT (MQTT over TLS).

---

## Installation og Opsætning af Mosquitto Broker

### Installation af broker og klienter (Debian/Ubuntu/Xubuntu):
```sh
sudo apt update
sudo apt install mosquitto mosquitto-clients -y
```

### Styr Mosquitto service:
```sh
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
sudo systemctl status mosquitto
```

---

## Demonstation med 3 Terminaler (Lokal test)

Man kan teste MQTT-flowet lokalt på sin maskine ved at dele skærmen i tre terminaler:

1.  **Terminal 1 (Se rå log):**
    Start brokeren manuelt i verbose mode for at overvåge forbindelser:
    ```sh
    mosquitto -v
    ```

2.  **Terminal 2 (Subscriber):**
    Tilmeld dig emnet `test` og vent på beskeder:
    ```sh
    mosquitto_sub -h localhost -t test -v
    ```

3.  **Terminal 3 (Publisher):**
    Send en besked til emnet `test`:
    ```sh
    mosquitto_pub -h localhost -t test -m "hello mqtt"
    ```

---

## Quality of Service (QoS)

MQTT understøtter tre pålidelighedsniveauer for levering af beskeder:

*   **QoS 0 (At most once / Fire and Forget):** Beskeden sendes én gang uden garanti for modtagelse. Hurtigst, men mindst pålidelig.
*   **QoS 1 (At least once):** Beskeden leveres mindst én gang. Publisher venter på en `PUBACK`-pakke fra brokeren. Hvis den ikke kommer, genudsendes beskeden.
*   **QoS 2 (Exactly once):** Beskeden leveres præcis én gang via en 4-vejs handshake (`PUBLISH` -> `PUBREC` -> `PUBREL` -> `PUBCOMP`). Mest pålidelig, men langsomst.

### Eksempel på Publish med QoS 1:
```sh
mosquitto_pub -h 172.20.10.12 -p 1883 -i TestKlientID -t esp32/temp -m "23.4" -q 1
```

---

## Fejlsøgning og Erfaringer

*   **Forbindelsesrækkefølge**: En C++ publisher må ikke antage at den kan sende med det samme. Den skal vente på, at brokeren bekræfter forbindelsen (CONNACK).
*   **Topic stavning**: Topics er case-sensitive, og et ekstra eller manglende `/` eller mellemrum ændrer kanalen (f.eks. `esp32/temp` vs `esp32/temp `).
*   **IP-Adresse**: Hvis ESP32 eller en remote klient skal forbinde, kan man ikke bruge `localhost` eller `127.0.0.1`. Man skal angive brokerens faktiske LAN IP (f.eks. `192.168.10.10`).

---

## Wireshark og Fejlfinding

### Display filters:
```text
mqtt
tcp.port == 1883
```

### Eksamensforklaring:
MQTT kører på applikationslaget. I Wireshark kan man se en TCP handshake (SYN, SYN-ACK, ACK) på port 1883 efterfulgt af en `Connect Command` fra klienten og et `Connect Ack` (CONNACK) fra brokeren. Derefter vil man kunne se `Publish Message` (hvor payloaden ofte kan læses i klartekst) og eventuelle QoS-kvitteringer som `PubAck`.
