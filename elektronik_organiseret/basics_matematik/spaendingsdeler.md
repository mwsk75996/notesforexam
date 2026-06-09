# Spændingsdeler

En spændingsdeler laver en lavere spænding ud fra to modstande.

```text
Vin -- R1 -- Vout -- R2 -- GND
```

Formel:

```text
Vout = Vin * R2 / (R1 + R2)
```

Den bruges ofte til:

- Potentiometer
- LDR lyssensor
- Simpel analog sensor
- At lave et signal som en ADC kan læse

Eksempel:

```text
Vin = 3.3V
R1 = 10k
R2 = 10k

Vout = 3.3V * 10k / (10k + 10k)
Vout = 1.65V
```
