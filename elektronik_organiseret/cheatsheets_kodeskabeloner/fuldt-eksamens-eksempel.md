# Fuldt Eksamens-eksempel: ESP32, OLED, MQTT og MariaDB

Dette dokument indeholder en komplet, fuldt funktionsdygtig løsning, der opfylder alle krav i **ITT2 Eksamen - Studerendes forberedelse** PDF-filen.

Løsningen består af:
1. **PlatformIO Projektopsætning** (`platformio.ini`).
2. **ESP32 Kode** (`src/main.cpp`) som forbinder til WiFi/MQTT, måler gas (MQ135/MQ2) og temperatur (DS18B20), udskriver på 1.3" OLED-displayet (SH1106) og sender data som JSON via MQTT.
3. **MariaDB SQL-skript** til oprettelse af databasen og den specifikke tabel.
4. **Shell Script** til PC3, der abonnerer på MQTT og indsætter data i MariaDB.

---

## 1. PlatformIO Opsætning (`platformio.ini`)

Opret et nyt PlatformIO projekt til ESP32, og erstat indholdet af `platformio.ini` med følgende:

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino

; Serial Monitor hastighed
monitor_speed = 115200

; Biblioteks-afhængigheder
lib_deps =
    olikraus/U8g2 @ ^2.35.19               ; Til 1.3" SH1106 OLED
    knolleary/PubSubClient @ ^2.8          ; Til MQTT
    paulstoffregen/OneWire @ ^2.3.8         ; Til DS18B20 temperatur-bus
    milesburton/DallasTemperature @ ^3.9.0   ; Til DS18B20 sensor-logik
```

---

## 2. ESP32 Firmware (`src/main.cpp`)

Forbindelser på din **ESP32 Wroom 38-Pin**:
- **OLED 1.3"**: `VCC` -> 3.3V, `GND` -> GND, `SDA` -> GPIO 21, `SCL` -> GPIO 22.
- **MQ135 / MQ2**: `VCC` -> 5V, `GND` -> GND, `AOUT` -> GPIO 33 (ADC1).
- **DS18B20**: `VCC` -> 3.3V, `GND` -> GND, `DATA` -> GPIO 19. *Husk $4.7\text{ k}\Omega$ modstand mellem DATA og 3.3V!*

```cpp
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <U8g2lib.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// WiFi og MQTT indstillinger
const char* ssid = "Dit_WiFi_Navn";
const char* password = "Dit_WiFi_Kodeord";
const char* mqtt_server = "192.168.1.100"; // Indtast PC3's IP (MQTT broker)
const char* mqtt_topic = "esp32/sensor_data";

// Hardware-pins
#define GAS_PIN 33       // MQ135/MQ2 AOUT tilsluttet GPIO33 (ADC1)
#define ONE_WIRE_BUS 19  // DS18B20 DATA tilsluttet GPIO19

// Initialisering af display (1.3" SH1106 I2C OLED)
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

// Initialisering af 1-Wire (DS18B20)
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensors(&oneWire);

// MQTT og WiFi Objekter
WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsgTime = 0;

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
    Serial.println("\nWiFi forbundet!");
    Serial.print("IP-adresse: ");
    Serial.println(WiFi.localIP());
}

void reconnect_mqtt() {
    while (!client.connected()) {
        Serial.print("Forsøger MQTT forbindelse...");
        String clientId = "ESP32_WROOM_1"; // Unikt Device ID
        
        if (client.connect(clientId.c_str())) {
            Serial.println("forbundet til broker!");
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
    
    // Start I2C og Display
    Wire.begin(21, 22);
    u8g2.begin();
    
    // Vis opstartsskærm
    u8g2.clearBuffer();
    u8g2.setFont(u8g2_font_ncenB08_tr);
    u8g2.drawStr(0, 20, "ESP32 Starter...");
    u8g2.sendBuffer();

    // Start temperatursensor
    tempSensors.begin();

    // WiFi og MQTT opsætning
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    
    Serial.println("Gassensor varmer op...");
    u8g2.clearBuffer();
    u8g2.drawStr(0, 20, "Varmer sensor op...");
    u8g2.sendBuffer();
    delay(5000); // Kortere delay til test (brug 30s+ i virkeligheden)
}

void loop() {
    if (!client.connected()) {
        reconnect_mqtt();
    }
    client.loop();

    unsigned long now = millis();
    if (now - lastMsgTime > 5000) { // Send måling hvert 5. sekund
        lastMsgTime = now;

        // 1. Læs temperatur (DS18B20)
        tempSensors.requestTemperatures();
        float tempC = tempSensors.getTempCByIndex(0);

        // 2. Læs Gas rå ADC (MQ135/MQ2)
        int gasRaw = analogRead(GAS_PIN);

        // Hvis temperatursensoren ikke svarer, sæt standardfejl
        if (tempC == DEVICE_DISCONNECTED_C) {
            tempC = 0.0;
            Serial.println("Fejl: DS18B20 ikke fundet.");
        }

        // 3. Opdater OLED Display
        u8g2.clearBuffer();
        u8g2.setFont(u8g2_font_ncenB08_tr);
        u8g2.drawStr(0, 15, "--- SENSORDATA ---");
        
        char tempStr[32];
        sprintf(tempStr, "Temp: %.2f C", tempC);
        u8g2.drawStr(0, 35, tempStr);
        
        char gasStr[32];
        sprintf(gasStr, "Gas rå: %d", gasRaw);
        u8g2.drawStr(0, 55, gasStr);
        u8g2.sendBuffer();

        // 4. Send JSON payload over MQTT
        // Payload form: {"temp": 24.50, "gas": 185, "device_id": "ESP32_WROOM_1"}
        String payload = "{";
        payload += "\"temp\":";
        payload += String(tempC, 2);
        payload += ",\"gas\":";
        payload += gasRaw;
        payload += ",\"device_id\":\"ESP32_WROOM_1\"";
        payload += "}";

        Serial.print("Sender MQTT payload: ");
        Serial.println(payload);
        client.publish(mqtt_topic, payload.c_str());
    }
}
```

---

## 3. MariaDB Database Setup (`database_setup.sql`)

Kør følgende SQL-kommandoer i din MariaDB terminal på PC'en for at oprette den database og tabelstruktur, som eksamensforberedelsen kræver:

```sql
-- Opret databasen
CREATE DATABASE IF NOT EXISTS Sensordata;
USE Sensordata;

-- Opret tabel med præcis de tre krævede kolonner:
-- 1. Temperaturmåling, 2. Tidsstempel, 3. Device ID
-- Vi bruger backticks ` ` for at tillade mellemrum i kolonnenavnet 'Device ID'
CREATE TABLE IF NOT EXISTS temperatur_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Temperaturmåling` DOUBLE NOT NULL,
    `Tidsstempel` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `Device ID` VARCHAR(50) NOT NULL
);

-- Vis tabellens struktur for at bekræfte
DESCRIBE temperatur_log;
```

---

## 4. Shell Script til PC3 (`mqtt_to_mariadb.sh`)

Dette shell script skal køre på din PC3 Linux-maskine. Scriptet lytter (subscribes) på MQTT topic `esp32/sensor_data`, modtager JSON payloads fra ESP32, udpakker værdierne og indsætter dem i MariaDB-databasen.

Scriptet bruger værktøjet **`jq`** til at parse JSON-data på en nem og robust måde. Du kan installere det på Xubuntu med `sudo apt update && sudo apt install jq`.

### Skriptets kode:
```bash
#!/bin/bash

# Konfiguration
MQTT_BROKER="localhost" # PC3's egen IP eller localhost
MQTT_TOPIC="esp32/sensor_data"
DB_USER="root"
DB_PASS="dit_mariadb_kodeord"
DB_NAME="Sensordata"
DB_TABLE="temperatur_log"

echo "Starter MQTT-til-MariaDB bro..."
echo "Abonnerer på topic: $MQTT_TOPIC"

# Lyt på MQTT bussen
mosquitto_sub -h "$MQTT_BROKER" -t "$MQTT_TOPIC" | while read -r line
do
    echo "Modtog data: $line"

    # Parse temperatur og device_id fra JSON ved hjælp af jq
    temp=$(echo "$line" | jq -r '.temp')
    device_id=$(echo "$line" | jq -r '.device_id')

    # Tjek om værdierne er valide (ikke tomme)
    if [ -n "$temp" ] && [ -n "$device_id" ]; then
        echo "Indsætter i database: Temp=$temp C, Device=$device_id"
        
        # Udfør MariaDB indsættelse (Tidsstempel indsættes automatisk via DEFAULT CURRENT_TIMESTAMP)
        mysql -u "$DB_USER" -p"$DB_PASS" -e \
        "INSERT INTO ${DB_NAME}.${DB_TABLE} (\`Temperaturmåling\`, \`Device ID\`) VALUES ($temp, '$device_id');"
        
        if [ $? -eq 0 ]; then
            echo "Indsættelse lykkedes!"
        else
            echo "Fejl ved databaseindsættelse!"
        fi
    else
        echo "Fejlagtig JSON payload modtaget - ignorerer."
    fi
    echo "--------------------------------------"
done
```

### Sådan gør du scriptet klar:
1. Gem scriptet som `mqtt_to_mariadb.sh` på din Linux maskine (PC3).
2. Gør scriptet eksekverbart i terminalen:
   ```bash
   chmod +x mqtt_to_mariadb.sh
   ```
3. Kør scriptet:
   ```bash
   ./mqtt_to_mariadb.sh
   ```
