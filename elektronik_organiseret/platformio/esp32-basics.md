# ESP32 basics

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
