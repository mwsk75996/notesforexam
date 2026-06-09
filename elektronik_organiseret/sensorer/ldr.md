# LDR - Lyssensor (Light Dependent Resistor)

## Beskrivelse
En LDR (foto-modstand) er en modstand, hvis resistans ændrer sig efter lysintensiteten.
- **I mørke**: Modstanden er meget høj (typisk flere megaohm, $\text{M}\Omega$).
- **I lys**: Modstanden falder drastisk (typisk ned til få hundrede ohm, $\Omega$).

Da en mikrokontroller ikke kan måle modstand direkte, skal en LDR altid indgå i en **spændingsdeler** sammen med en fast modstand (typisk $10\text{ k}\Omega$). Dette omsætter modstandsændringen til en variabel analog spænding, som kan måles med ESP32'erens ADC.

### Spændingsdeler-placering og signalretning (Eksamen!)
Retningen på dit signal (om spændingen stiger eller falder ved lys) afhænger af, hvordan du placerer modstandene:

1. **LDR forbundet til VCC (Pull-down konfiguration)**:
   ```text
   VCC (3.3V) --- [ LDR ] --- GPIO (Analog In) --- [ 10k modstand ] --- GND
   ```
   - **Når lyset stiger**: Modstanden i LDR falder. LDR leder strømmen bedre. Spændingen på GPIO-pinden **stiger** (går mod 3.3V).
   - **Formel**: $V_{out} = V_{in} \cdot \frac{10\text{k}}{R_{LDR} + 10\text{k}}$

2. **LDR forbundet til GND (Pull-up konfiguration)**:
   ```text
   VCC (3.3V) --- [ 10k modstand ] --- GPIO (Analog In) --- [ LDR ] --- GND
   ```
   - **Når lyset stiger**: Modstanden i LDR falder. LDR trækker signalet tættere til GND. Spændingen på GPIO-pinden **falder** (går mod 0V).
   - **Formel**: $V_{out} = V_{in} \cdot \frac{R_{LDR}}{10\text{k} + R_{LDR}}$

---

## Kodeeksempel (PlatformIO / Arduino C++)
Eksemplet antager en Pull-down konfiguration (LDR til VCC, 10k til GND), så lys giver højere værdier:

```cpp
#include <Arduino.h>

const int ldrPin = 34;       // Analog input (GPIO34 er ADC1)
const int ledPin = 12;       // LED til indikering (blå LED)
const int darkThreshold = 1500; // Kalibreret grænseværdi for mørke

void setup() {
    Serial.begin(115200);
    pinMode(ldrPin, INPUT);
    pinMode(ledPin, OUTPUT);
    Serial.println("LDR lyssensor klar!");
}

void loop() {
    int rawValue = analogRead(ldrPin); // Læs rå ADC værdi (0-4095)
    float voltage = rawValue * 3.3 / 4095.0; // Beregn spænding
    
    Serial.print("Rå ADC: ");
    Serial.print(rawValue);
    Serial.print("  |  Spænding: ");
    Serial.print(voltage);
    Serial.println(" V");

    // Hvis lysniveauet falder under grænsen, tændes lyset (natlampe)
    if (rawValue < darkThreshold) {
        digitalWrite(ledPin, HIGH);
        Serial.println("Status: MØRKT - Tænder LED!");
    } else {
        digitalWrite(ledPin, LOW);
        Serial.println("Status: LYST - Slukker LED.");
    }

    delay(1000);
}
```

---

## Typiske fejl og eksamensspørgsmål
- **Hvorfor flyver værdierne tilfældigt?**: Hvis spændingsdeleren mangler den faste modstand (10k), vil analog pin "flyde". Det giver tilfældige værdier på ADC'en.
- **Hvordan vælges værdien af den faste modstand?**: Modstanden skal vælges således, at den er tæt på LDR'ens modstand i det arbejdsområde (lysforhold), du vil måle i. Typisk er $10\text{ k}\Omega$ det bedste kompromis til normalt dagslys/stuelys.
- **Hvilken pin skal bruges på ESP32?**: GPIO34-39 (ADC1) er perfekte til LDR, da de er input-only og virker stabilt sammen med WiFi.
