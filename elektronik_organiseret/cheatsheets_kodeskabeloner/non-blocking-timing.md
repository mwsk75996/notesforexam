# Blink uden delay (Non-blocking timing)

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
