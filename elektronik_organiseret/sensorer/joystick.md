# Joystick - Analog og Digital Styring

## Beskrivelse
Et analogt joystick (fx det der bruges til rover-styring) består af tre hoveddele samlet i én komponent:
1. **X-akse potentiometer**: En analog spændingsdeler, der ændrer spænding ved vandret bevægelse.
2. **Y-akse potentiometer**: En analog spændingsdeler, der ændrer spænding ved lodret bevægelse.
3. **Z-akse (knap)**: En digital taktil switch (knap), der aktiveres, når man trykker lodret ned på joysticket.

### Hvordan det fungerer:
- Potentiometrene er forbundet til $V_{CC}$ ($3.3\text{V}$) og GND. Midtpunkterne (sliderne) leverer en spænding.
- Når joysticket står i midten (neutral position), leveres ca. halvdelen af forsyningsspændingen ($1.65\text{V}$), hvilket svarer til en rå ADC-værdi på ca. **`2048`** på ESP32.
- Ved fuldt udslag i den ene retning går spændingen mod $0\text{V}$ (ADC $\approx 0$).
- Ved fuldt udslag i den anden retning går spændingen mod $3.3\text{V}$ (ADC $\approx 4095$).

### Ledningsforbindelse (Wiring):
- **VCC**: 3.3V
- **GND**: GND (Fælles stel)
- **VRX (X-akse)**: Analog GPIO pin (fx GPIO 34 - ADC1)
- **VRY (Y-akse)**: Analog GPIO pin (fx GPIO 35 - ADC1)
- **SW (Knap)**: Digital GPIO pin (fx GPIO 32 - kræver Pull-up modstand)

---

## Kodeeksempel (PlatformIO / Arduino C++)
```cpp
#include <Arduino.h>

const int pinX = 34;  // VRX tilsluttet analog pin GPIO34 (ADC1)
const int pinY = 35;  // VRY tilsluttet analog pin GPIO35 (ADC1)
const int pinSW = 32; // SW tilsluttet digital pin GPIO32

void setup() {
    Serial.begin(115200);
    
    pinMode(pinX, INPUT);
    pinMode(pinY, INPUT);
    
    // Knappen på joysticket forbinder til GND når den trykkes.
    // Vi aktiverer ESP32'erens interne pull-up modstand, så signalet 
    // som udgangspunkt læses som HIGH (1), og går LOW (0) ved tryk.
    pinMode(pinSW, INPUT_PULLUP);
    
    Serial.println("Joystick initialiseret!");
}

void loop() {
    int xValue = analogRead(pinX); // Læs X-akse (0-4095)
    int yValue = analogRead(pinY); // Læs Y-akse (0-4095)
    int btnState = digitalRead(pinSW); // Læs knap (0 = trykket, 1 = neutral)

    Serial.print("Joystick X (Vandret): ");
    Serial.print(xValue);
    Serial.print("  |  Y (Lodret): ");
    Serial.print(yValue);
    
    if (btnState == LOW) {
        Serial.print("  |  KNAP TRYKKET!");
    }
    Serial.println();

    // Simpel retnings-debugging (Deadzone på +-300 omkring midten 2048)
    if (xValue < 1700) {
        Serial.println("Retning: VENSTRE");
    } else if (xValue > 2300) {
        Serial.println("Retning: HØJRE");
    }

    if (yValue < 1700) {
        Serial.println("Retning: NED / BAGUD");
    } else if (yValue > 2300) {
        Serial.println("Retning: OP / FREMAD");
    }

    delay(500);
}
```

---

## Typiske fejl og eksamensspørgsmål
- **Hvorfor aflæser vi værdier omkring 0 og 4095 tilfældigt, når knappen ikke er trykket?**: Hvis du indstiller `pinMode(pinSW, INPUT)` uden pull-up, vil pinnen "flyde" i ubestemt tilstand, når knappen ikke er trykket (fordi knappen bare hænger i luften og ikke er forbundet til noget). Ved at bruge `INPUT_PULLUP` sikrer vi, at pinnen har en svag intern modstand til 3.3V, så den læser et stabilt HIGH, indtil knappen fysisk trækker pinnen til GND (LOW).
- **Hvad er formålet med en "Deadzone" i koden?**: Da billige potentiometre i joysticks ikke er helt perfekte, vil de sjældent returnere præcis 2048 i neutral position. Værdien vil måske svinge mellem 2010 og 2090. Hvis vi ikke definerer en "død zone" (deadzone) i koden, vil roveren tro, at joysticket trykkes svagt, selvom det står helt stille.
