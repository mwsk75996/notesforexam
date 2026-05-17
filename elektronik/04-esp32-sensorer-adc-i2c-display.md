# ESP32, sensorer, ADC, I2C og display

## ESP32 basics

ESP32 er en mikrocontroller med:

- GPIO pins
- WiFi og Bluetooth
- ADC til analoge signaler
- I2C/SPI/UART til sensorer
- PWM output

Repo-eksempler:

- [ass62network](https://github.com/mwsk75996/ass62network) - ESP32 med DS18B20 temperatur-sensor og MQTT publish
- [g8 Rover projekt](https://github.com/mwsk75996/g8) - PlatformIO-projekt med ESP32, sensorer og rover-kode

Vigtigt:

- ESP32 GPIO er normalt `3.3V`.
- Giv ikke `5V` direkte ind på en GPIO.
- Sensorer skal have fælles `GND` med ESP32.

## Analog input

Analog input bruges til sensorer der giver en spænding.

Eksempel:

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

På ESP32 er ADC-værdier ofte cirka:

```text
0V    -> 0
3.3V  -> 4095
```

I praksis er ADC på ESP32 ikke perfekt lineær, så rå værdier bør kalibreres.

## I2C

I2C bruges ofte til sensorer og OLED display.

Typiske pins på ESP32:

```text
SDA = GPIO 21
SCL = GPIO 22
```

Eksempler på I2C-enheder fra opgaverne:

- BMP280 tryk/temperatur
- OLED display
- GY-521 MPU6050 accelerometer/gyro
- HMC5883L / GY-271 kompas
- ADS1115 ADC

Typisk kode:

```cpp
#include <Wire.h>

void setup() {
    Wire.begin();
}
```

## OLED display

OLED bruges til at vise målinger uden at være afhængig af serial monitor.

Typisk vises:

- Temperatur
- Fugtighed
- Tryk
- Afstand
- Komfort-score
- Sensorstatus

God eksamensforklaring:

> Serial monitor er god til debugging, men OLED gør systemet mere selvstændigt, fordi brugeren kan aflæse værdier direkte på enheden.

## Normalisering

Normalisering betyder at man laver forskellige målinger om til samme skala, fx `0-100`.

Eksempel:

```cpp
int normalize(float value, float minValue, float maxValue) {
    float normalized = (value - minValue) * 100.0 / (maxValue - minValue);
    return constrain(normalized, 0, 100);
}
```

Det er nyttigt når man vil kombinere flere sensorer til én score.

Eksempel fra indeklima:

```text
DHT11 temperatur
BMP280 temperatur
Fugtighed
Tryk

-> normaliseres
-> vægtes
-> komfort-score
```

## JSON fra ESP32

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

## ESP32 MQTT sensor pattern

Fra `ass62network`:

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
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
