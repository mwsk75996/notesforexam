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

## Komfort-score

```cpp
float score =
    tempScore * 0.5 +
    humidityScore * 0.3 +
    pressureScore * 0.2;
```

## Typiske formler

```text
U = R * I
I = U / R
R = U / I

P = U * I

Vout = Vin * R2 / (R1 + R2)

tau = R * C

driftstid = mAh / mA
```

## Typiske ESP32 pins fra opgaverne

```text
I2C SDA: GPIO 21
I2C SCL: GPIO 22

MQ-135 AOUT: GPIO 33
LDR analog:  GPIO 34

Grøn LED: GPIO 26
Gul LED:  GPIO 27
Rød LED:  GPIO 14
Blå LED:  GPIO 12
```

## Hurtig fejlfinding

Tjek først:

- Er der fælles GND?
- Er sensoren på rigtig spænding?
- Er GPIO-pinnen korrekt i koden?
- Er `Serial.begin(115200)` og serial monitor samme baud rate?
- Er I2C-ledninger byttet rundt?
- Er sensorens adresse korrekt?
- Hopper rå værdier, så der skal kalibreres eller filtreres?

## Gode eksamenssætninger

> Jeg starter med at læse rå værdier i serial monitor, fordi thresholds først giver mening når jeg kender sensorens faktiske måleområde.

> ESP32 bruger 3.3V logik, så jeg skal passe på ikke at sende 5V direkte ind på en GPIO.

> Hvis målingen hopper meget, kan jeg enten filtrere i hardware med RC/kondensator eller i software med gennemsnit.

> Oscilloskopet bruges når jeg vil se det elektriske signal direkte, især PWM, støj og timing.

> Et OLED display gør systemet mere selvstændigt, fordi værdierne kan aflæses uden PC.
