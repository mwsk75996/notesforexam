# Threshold med LED

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


## MQ135 / MQ2 Gassensor & LED Tresholds

Kodeeksempel med opvarmningsfase (heater), analog læsning og LED-indikering:

```cpp

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
