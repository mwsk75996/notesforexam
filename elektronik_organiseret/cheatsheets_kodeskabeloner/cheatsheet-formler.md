# Serial debug

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
