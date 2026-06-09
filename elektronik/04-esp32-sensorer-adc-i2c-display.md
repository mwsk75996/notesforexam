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

### Fra ADC-værdi til spænding

ADC'en laver en analog spænding om til et tal.

Hvis man antager `0-3.3V` og `0-4095`, kan man estimere spændingen:

```cpp
int raw = analogRead(34);
float voltage = raw * 3.3 / 4095.0;

Serial.print("raw=");
Serial.print(raw);
Serial.print(" voltage=");
Serial.println(voltage);
```

Eksempel:

```text
raw = 2048
voltage = 2048 * 3.3 / 4095
voltage = cirka 1.65V
```

God eksamensforklaring:

> ESP32 læser ikke direkte "temperatur" eller "lys". Den læser en spænding på ADC-pinnen. Koden oversætter den rå ADC-værdi til noget meningsfuldt med kalibrering, thresholds eller en sensor-formel.

### Hvorfor kalibrering er vigtigt

To ens sensorer giver ikke altid præcis samme rå værdi. Målingen afhænger af:

- sensorens tolerancer
- forsyningsspænding
- ledninger og støj
- placering og miljø
- ESP32 ADC unøjagtighed

Derfor tester man først rå værdier:

```cpp
void loop() {
    int raw = analogRead(34);
    Serial.println(raw);
    delay(200);
}
```

Derefter vælger man thresholds ud fra rigtige målinger:

```text
mørkt rum:       800-1200
normal belysning: 1800-2500
stærkt lys:      3000+
```

Så kan en threshold fx vælges som:

```cpp
if (lightValue < 1500) {
    Serial.println("for mørkt");
}
```

### Floating input

Hvis en analog pin ikke er forbundet til et stabilt signal, kan den "flyde". Så hopper værdien tilfældigt.

Typiske symptomer:

```text
raw: 381
raw: 2900
raw: 74
raw: 1800
```

Løsning:

- brug en rigtig spændingsdeler
- brug pull-up eller pull-down hvor det giver mening
- tjek fælles GND
- hold ledninger korte ved analoge signaler

### Gode ADC pins på ESP32

Til analog input bruges ofte ADC1 pins, fx:

```text
GPIO32
GPIO33
GPIO34
GPIO35
GPIO36
GPIO39
```

GPIO34-39 er input-only. De kan læse analogt, men kan ikke bruges som almindeligt output.

Vigtigt med WiFi:

> På mange ESP32 boards kan ADC2 give problemer mens WiFi er aktivt. Derfor er ADC1 pins ofte det sikreste valg til sensorer i WiFi-projekter.

## ESP32 Wroom 38-Pin Pinout og Hardware-layout

ESP32 Wroom 38-Pin er det specifikke board til eksamen. Det er vigtigt at kende dets pin-grupper:
- **Strømforsyning**:
  - `VIN / 5V`: Ekstern 5V spændingsindgang (eller strøm fra USB-C).
  - `3.3V`: Output fra den indbyggede LDO regulator (må max belastes med ca. 500-800mA til delte sensorer).
  - `GND`: Fælles stel (Ground).
- **Analog Input (ADC)**:
  - **ADC1**: GPIO32-39. **Disse er sikre at bruge når WiFi kører.**
  - **ADC2**: GPIO0, 2, 4, 12-15, 25-27. *Kan IKKE bruges stabilt samtidigt med at WiFi-senderen er aktiv.*
  - **Input-Only Pins**: GPIO34, 35, 36 (VP), 39 (VN) har ingen interne pull-up/pull-down modstande og kan **kun** bruges som input.
- **Kommunikations-pins (Default)**:
  - **I2C**: SDA (GPIO21), SCL (GPIO22).
  - **SPI (VSPI)**: MOSI (GPIO23), MISO (GPIO19), SCLK (GPIO18), CS (GPIO5).
  - **UART0 (USB debug)**: TX (GPIO1), RX (GPIO3).
  - **UART2**: TX2 (GPIO17), RX2 (GPIO16).

---

## Kommunikationsprotokoller: I2C, SPI, UART

Når mikrokontrolleren snakker med sensorer og displays, bruges seriel kommunikation. Protokollerne adskiller sig på hastighed, antal ledninger og netværksstruktur.

### Transmissionsretninger (Duplex-tilstande)
1. **Simplex**: Én-vejs kommunikation. Data sendes kun fra sender til modtager (fx en simpel temperatursensor med en enkelt data-ledning, der kun sender).
2. **Half-duplex**: To-vejs kommunikation, men **kun én retning ad gangen**. Enhederne skal skiftes til at sende og modtage på samme linje (fx I2C).
3. **Full-duplex**: Simultan to-vejs kommunikation. Begge enheder kan sende og modtage samtidigt, typisk via to separate ledninger (fx UART og SPI).

### Sammenligningstabel for protokoller:

| Protokol | Type | Ledninger (ex. strøm) | Duplex | Hastighed | Enheder (Netværk) | Pull-up påkrævet? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UART** | Asynkron (intet clock-signal) | 2 (TX, RX) | Full-duplex | Langsom til medium (typisk 115200 bps) | Point-to-Point (kun 2 enheder) | Nej (normalt drevet aktivt) |
| **I2C** | Synkron (clock-styret) | 2 (SDA, SCL) | Half-duplex | Medium (100 kHz - 400 kHz) | Multi-master / Multi-slave (adresse-baseret) | **Ja** (SDA/SCL skal have pull-up modstande til VCC, typisk 4.7k$\Omega$) |
| **SPI** | Synkron | 3-4+ (MOSI, MISO, SCK, CS/SS) | Full-duplex | Meget hurtig (flere MHz) | 1 Master, flere slaves (kræver en CS-linje pr. slave) | Nej |

---

## I2C detaljer på ESP32

I2C (Inter-Integrated Circuit) bruges til at forbinde mange sensorer på de samme to ledninger. Hver enhed har en unik hex-adresse (fx `0x3C` eller `0x76`).

Eksempler på I2C-enheder:
- **BMP280** tryk/temperatur (typisk adresse `0x76` eller `0x77`)
- **Display OLED 1.3”** (typisk adresse `0x3C`)
- **GY-521 MPU6050** accelerometer/gyro (typisk adresse `0x68`)
- **ADS1115** ekstern ADC (typisk adresse `0x48`)

### Hvorfor Pull-up modstande på I2C?
I2C-bussen bruger "open-drain" udgange. Det betyder, at enhederne kun kan trække signalet aktivt **LOW** (til GND). De kan ikke tvinge linjen HIGH. Derfor skal der være eksterne **pull-up modstande** (fx $4.7\text{ k}\Omega$) til $3.3\text{V}$ på både `SDA` og `SCL`. Uden dem vil signalet forblive LOW, og kommunikationen fejler. De fleste sensor-breakoutboards har disse modstande indbygget.

---

## OLED display 1.3” I2C (SH1106)

Til eksamen skal der medbringes et **Display OLED 1.3” I2C 128x64**. 
- **Vigtig forskel**: Standard 0.96" displayet bruger normalt en `SSD1306` driver, men det større 1.3" display bruger næsten altid en **SH1106** driver.
- Hvis du bruger et SSD1306-bibliotek til en SH1106, vil skærmen ofte være forskudt med 2 pixels i siderne eller vise "sne" (støj).
- **Løsning i PlatformIO**: Brug `U8g2` biblioteket. Det understøtter SH1106 direkte og er meget stabilt.

### U8g2 initialisering af 1.3" I2C OLED (SH1106):
```cpp
#include <Arduino.h>
#include <U8g2lib.h>
#include <Wire.h>

// SH1106 driver til 128x64 I2C skærm. 
// U8G2_R0 = ingen rotation, F = Full framebuffer (kræver lidt RAM), HW_I2C = hardware I2C pins.
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void setup() {
    // Start I2C med standard pins SDA=21, SCL=22
    Wire.begin(21, 22);
    
    // Start displayet
    u8g2.begin();
}

void loop() {
    u8g2.clearBuffer();          // Ryd skærm-bufferen
    u8g2.setFont(u8g2_font_ncenB08_tr); // Vælg skrifttype
    u8g2.drawStr(0, 15, "Temperatur: 24.5 C");
    u8g2.drawStr(0, 30, "Gas: OK");
    u8g2.sendBuffer();           // Send bufferen til skærmen
    delay(1000);
}
```

**God eksamensforklaring**:
> Serial monitor er god til debugging, men OLED-displayet gør systemet selvstændigt. Ved at bruge I2C-bussen (SDA/SCL) kan vi dele ledninger med andre I2C-sensorer (fx BMP280), så vi sparer GPIO-pins på ESP32. Da displayet er 1.3", bruger vi SH1106-driveren i U8g2-biblioteket for at undgå pixel-forskydning.

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
