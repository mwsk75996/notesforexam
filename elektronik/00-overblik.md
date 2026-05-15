# Indlejrede systemer og elektronik - overblik

De her noter er lavet ud fra opgaverne i `Indlejrede Eksempler`.

De vigtigste emner der går igen:

- Ohms lov, effekt og modstande
- Spændingsdeler, Wheatstonebro og Thevenin
- Batterier, regulatorer, PWM og strømforbrug
- ESP32, GPIO, ADC, I2C og OLED display
- Sensorer som DHT11, BMP280, MQ-135, LDR, GY-521 og HMC5883L
- Støj, filtre og oscilloskop
- RC-kredsløb og 555 timer
- Binær talforståelse og logiske gates
- Kalibrering, thresholds og fejlfinding

God eksamensstruktur når du skal forklare en opgave:

1. Forklar hvad systemet skal måle eller styre.
2. Vis hvilke komponenter der er med.
3. Forklar signalet: analogt, digitalt, I2C, PWM osv.
4. Forklar beregningen: formel, threshold eller normalisering.
5. Vis hvordan det testes: multimeter, serial monitor, oscilloskop eller output.
6. Fortæl hvad der kan give fejl: støj, forkert pin, forkert spænding, dårlig kalibrering.

Gode standard tests:

```cpp
Serial.begin(115200);
Serial.println("starter...");
```

```cpp
int value = analogRead(34);
Serial.println(value);
```

```sh
pio device monitor
```

eller i Arduino IDE:

```text
Tools -> Serial Monitor
Baud rate: 115200
```

Typiske ting at nævne:

- ESP32 GPIO bruger normalt 3.3V logik.
- Mange sensorer bruger I2C med `SDA` og `SCL`.
- Analog input på ESP32 læses ofte som cirka `0-4095`.
- En sensor skal ofte kalibreres med rå værdier før thresholds giver mening.
- Et multimeter bruges til DC-spænding, modstand og kontinuitet.
- Et oscilloskop bruges til signalform, støj, PWM og timing.
