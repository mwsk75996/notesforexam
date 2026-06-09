# Mini templates og cheatsheet

## Serial debug

```cpp
void setup() {
    Serial.begin(115200);
}

void loop() {
    Serial.println("test");
    delay(500);
}
```

## Analog sensor

```cpp
const int sensorPin = 34;

void setup() {
    Serial.begin(115200);
}

void loop() {
    int value = analogRead(sensorPin);
    Serial.println(value);
    delay(500);
}
```

## Threshold med LED

```cpp
const int sensorPin = 34;
const int ledPin = 12;
const int threshold = 2500;

void setup() {
    Serial.begin(115200);
    pinMode(ledPin, OUTPUT);
}

void loop() {
    int value = analogRead(sensorPin);

    if (value < threshold) {
        digitalWrite(ledPin, HIGH);
    } else {
        digitalWrite(ledPin, LOW);
    }

    Serial.println(value);
    delay(250);
}
```

## Blink uden sensor

```cpp
const int ledPin = 26;

void setup() {
    pinMode(ledPin, OUTPUT);
}

void loop() {
    digitalWrite(ledPin, HIGH);
    delay(500);
    digitalWrite(ledPin, LOW);
    delay(500);
}
```

## Simpelt gennemsnit

```cpp
int readAverage(int pin) {
    int sum = 0;

    for (int i = 0; i < 10; i++) {
        sum += analogRead(pin);
        delay(5);
    }

    return sum / 10;
}
```

## Normalisering 0-100

```cpp
int normalize(float value, float minValue, float maxValue) {
    float normalized = (value - minValue) * 100.0 / (maxValue - minValue);
    return constrain(normalized, 0, 100);
}
```

## Blink uden delay (Non-blocking timing)

Undgå `delay()`, da det fryser mikrokontrolleren. Brug `millis()` til multitasking (fx læse sensorer hurtigt mens en LED blinker):

```cpp
const int ledPin = 26;
unsigned long previousMillis = 0;
const long interval = 500; // blink interval (ms)
int ledState = LOW;

void setup() {
    pinMode(ledPin, OUTPUT);
}

void loop() {
    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis; // Gem sidste tidspunkt

        // Skift tilstand på LED
        ledState = (ledState == LOW) ? HIGH : LOW;
        digitalWrite(ledPin, ledState);
    }
    
    // Her kan læses sensorer uden afbrydelse...
}
```

---

## platformio.ini Skabelon (ESP32 Wroom 38-Pin)

Konfiguration til PlatformIO-projektet til eksamen. Lægger biblioteker ind automatisk.

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino

; Serial Monitor indstillinger
monitor_speed = 115200
monitor_filters = esp32_exception_decoder

; Biblioteks-afhængigheder (installeres automatisk ved compile)
lib_deps =
    olikraus/U8g2 @ ^2.35.19             ; Til 1.3" SH1106 OLED display
    knolleary/PubSubClient @ ^2.8        ; Til MQTT kommunikation
    milesburton/DallasTemperature @ ^3.9.0 ; Til DS18B20 temp (hvis relevant)
```

---

## MQ135 / MQ2 Gassensor & LED Tresholds

Kodeeksempel med opvarmningsfase (heater), analog læsning og LED-indikering:

```cpp
#include <Arduino.h>

const int gasPin = 33;    // AOUT på GPIO33 (ADC1)
const int ledGreen = 26;  // God luft
const int ledYellow = 27; // Moderat
const int ledRed = 14;    // Dårlig

void setup() {
    Serial.begin(115200);
    pinMode(ledGreen, OUTPUT);
    pinMode(ledYellow, OUTPUT);
    pinMode(ledRed, OUTPUT);

    Serial.println("Varmer gassensor op... Vent 30 sek.");
    // Tænd alle LED under opvarmning som status
    digitalWrite(ledGreen, HIGH);
    digitalWrite(ledYellow, HIGH);
    digitalWrite(ledRed, HIGH);
    
    delay(30000); // 30s warm-up (anbefales 2 min i virkeligheden)
    
    digitalWrite(ledGreen, LOW);
    digitalWrite(ledYellow, LOW);
    digitalWrite(ledRed, LOW);
    Serial.println("Opvarmning færdig!");
}

void loop() {
    int rawValue = analogRead(gasPin);
    Serial.print("Gas rå værdi: ");
    Serial.println(rawValue);

    // Styr LED ud fra thresholds
    if (rawValue < 200) {
        digitalWrite(ledGreen, HIGH);
        digitalWrite(ledYellow, LOW);
        digitalWrite(ledRed, LOW);
    } 
    else if (rawValue >= 200 && rawValue <= 250) {
        digitalWrite(ledGreen, LOW);
        digitalWrite(ledYellow, HIGH);
        digitalWrite(ledRed, LOW);
    } 
    else { // rawValue > 250
        digitalWrite(ledGreen, LOW);
        digitalWrite(ledYellow, LOW);
        digitalWrite(ledRed, HIGH);
    }

    delay(1000);
}
```

---

## ESP32 WiFi & MQTT (PubSubClient) med JSON

Komplet skabelon til at forbinde til eksamens-brokeren, modtage/sende data og sende JSON payloads.

```cpp
#include <WiFi.h>
#include <PubSubClient.h>

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

## Typiske ESP32 pins fra opgaverne

```text
I2C SDA: GPIO 21
I2C SCL: GPIO 22

MQ-135/MQ-2 AOUT: GPIO 33
LDR analog:       GPIO 34

Grøn LED: GPIO 26
Gul LED:  GPIO 27
Rød LED:  GPIO 14
Blå LED:  GPIO 12
```

## Hurtig fejlfinding

Tjek først:
- **Er der fælles GND?** (Absolut mest almindelige fejl ved delte strømforsyninger).
- Er sensoren på den rigtige forsyningsspænding? (MQ-sensorer skal have 5V for at heateren virker optimalt, men AOUT måles på ESP32 3.3V logik; brug spændingsdeler hvis spændingen er for høj).
- Er GPIO-pinnen angivet korrekt i koden (GPIO-nummer, *ikke* det fysiske ben-nummer på chippen)?
- Er `Serial.begin(115200)` og Serial Monitor sat til samme baud rate?
- Er I2C-ledningerne (`SDA` og `SCL`) byttet rundt?
- Bruger du SH1106 driveren til det 1.3" OLED-display, eller SSD1306?
- Har du installeret korrekte USB-til-Serial drivere (CH340 eller CP210x)?

## Gode eksamenssætninger

> Jeg starter med at læse rå værdier i serial monitor, fordi thresholds først giver mening når jeg kender sensorens faktiske måleområde.

> ESP32 bruger 3.3V logik, så jeg skal passe på ikke at sende 5V direkte ind på en GPIO.

> Hvis målingen hopper meget, kan jeg enten filtrere i hardware med en kondensator (RC-filter) eller i software med et glidende gennemsnit.

> Oscilloskopet bruges, når jeg vil se det elektriske signal direkte i realtid for at analysere støj, timing og PWM-perioder.

> Et OLED-display gør systemet selvstændigt, fordi brugeren kan aflæse sensorværdier direkte på enheden uden at være tilsluttet en computer.
