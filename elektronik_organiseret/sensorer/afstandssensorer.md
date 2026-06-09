# Afstandssensorer: Ultralyd og Time-of-Flight

Afstandsmåling kan udføres ved hjælp af enten lydbølger (ultralyd) eller lyspartikler (laser/infrarød).

---

## 1. Ultralydssensor (fx HC-SR04)

### Beskrivelse
HC-SR04 måler afstand ved at udsende en højfrekvent lydbølge (ultralyd) og måle tiden, det tager for ekkoet at returnere fra en genstand.

### Den kritiske 5V-til-3.3V spændingsfælde (Eksamen!)
- HC-SR04 skal forsynes med **5V** for at fungere pålideligt.
- Dette betyder, at dens `ECHO` udgangssignal leverer en **5V logik**.
- Da ESP32 kun tåler **3.3V** på sine GPIO-pins, vil en direkte forbindelse ødelægge ESP32 over tid!
- **Løsning**: Du skal placere en **spændingsdeler** på `ECHO`-ledningen (fx en $1\text{ k}\Omega$ modstand i serie og en $2\text{ k}\Omega$ modstand mod GND) for at dæmpe spændingen fra 5V til ca. 3.3V inden den rammer ESP32. `TRIG` pin kan tilsluttes direkte til ESP32, da sensoren accepterer 3.3V logik som input.

### Ledningsforbindelse (Wiring med spændingsdeler):
- **VCC**: 5V
- **GND**: GND (Fælles stel)
- **TRIG**: GPIO pin (fx GPIO 13) -> Direkte til ESP32.
- **ECHO**: GPIO pin (fx GPIO 12) -> **Forbindes via spændingsdeler**.

### Kodeeksempel: HC-SR04 (Uden eksterne biblioteker)
```cpp
#include <Arduino.h>

const int trigPin = 13;
const int echoPin = 12; // Skal forbindes via spændingsdeler!

void setup() {
    Serial.begin(115200);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

void loop() {
    // Send en ren 10 mikrosekunders puls på TRIG
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Mål varigheden af ECHO-pulsen i mikrosekunder
    long duration = pulseIn(echoPin, HIGH);

    // Beregn afstand i cm ud fra lydens hastighed (343 m/s = 0.0343 cm/us)
    // Divideres med 2 fordi lyden rejser frem og tilbage
    float distance = duration * 0.0343 / 2.0;

    // HC-SR04 arbejder bedst inden for 2 - 400 cm
    if (distance >= 400 || distance <= 2) {
        Serial.println("Afstand: Uden for rækkevidde!");
    } else {
        Serial.print("Afstand (Ultralyd): ");
        Serial.print(distance);
        Serial.println(" cm");
    }

    delay(500);
}
```

---

## 2. Time-of-Flight Laser Sensor (fx VL53L0X)

### Beskrivelse
VL53L0X er en avanceret lasersensor. Den udsender en usynlig infrarød laserpuls og måler den præcise tid (lysets hastighed), det tager for fotonerne at reflektere tilbage. Den kommunikerer via I2C og giver millimeterpræcision.

### Ledningsforbindelse (I2C Wiring):
- **VCC**: 3.3V
- **GND**: GND (Fælles stel)
- **SDA**: GPIO 21 (ESP32 standard SDA)
- **SCL**: GPIO 22 (ESP32 standard SCL)

### Kodeeksempel: VL53L0X
Kræver `Adafruit_VL53L0X` i `platformio.ini`:
```ini
lib_deps =
    adafruit/Adafruit_VL53L0X @ ^1.2.4
```

```cpp
#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_VL53L0X.h>

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup() {
    Serial.begin(115200);
    Wire.begin(21, 22);

    Serial.println("Initialiserer VL53L0X...");
    if (!lox.begin()) {
        Serial.println("Kunne ikke finde VL53L0X sensor! Tjek ledninger.");
        while (1);
    }
    Serial.println("VL53L0X klar!");
}

void loop() {
    VL53L0X_RangingMeasurementData_t measure;

    // Tag en måling
    lox.rangingTest(&measure, false); 

    // Fase 4: Tjek om målingen var succesfuld
    if (measure.RangeStatus != 4) {  // Status 4 betyder "Out of range"
        Serial.print("Afstand (Laser): ");
        Serial.print(measure.RangeMilliMeter); // Målt i mm!
        Serial.println(" mm");
    } else {
        Serial.println("Afstand: Uden for rækkevidde!");
    }

    delay(500);
}
```

---

## Typiske fejl og eksamensspørgsmål
- **Hvorfor er ultralydssensoren upålidelig på bløde overflader?**: Ultralyd er en trykbølge i luften. Bløde materialer (fx tøj eller skum) absorberer lydbølgen i stedet for at reflektere den. Skrå overflader kaster ekkoet væk fra modtageren, så sensoren tror, der er tomt.
- **Hvorfor fejler lasersensoren i stærkt sollys?**: ToF-sensoren bruger infrarødt lys. Sollys indeholder enorme mængder infrarød stråling, som kan blænde sensorens modtager og drukne signalet i støj.
- **Hvordan beregnes afstanden for ultralyd?**: Formlen er $d = \frac{v \cdot t}{2}$. Vi kender lydens hastighed $v \approx 343\text{ m/s}$ (ved stuetemperatur). Tiden $t$ måles af mikrokontrolleren. Vi dividerer med 2, da lyden har tilbagelagt afstanden to gange.
- **Logikniveauer (ECHO)**: Husk at redegøre for spændingsdeleren på ECHO-pinnen. Det viser stor hardwareforståelse!
