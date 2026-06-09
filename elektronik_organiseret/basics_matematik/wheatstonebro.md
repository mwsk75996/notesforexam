# Wheatstonebro

En Wheatstonebro bruges til at måle meget små ændringer i modstand med høj præcision (fx i strain gauges, vægtceller/load cells eller præcise temperaturmålinger).

Broen består af to parallelle spændingsdelere forbundet til samme spændingskilde ($V_{in}$). Vi måler spændingsforskellen ($V_G$) mellem de to midtpunkter A og B:

```text
       Vin
      /   \
     R1   R3
     /     \
    A-------B  <-- Mål VG (spændingsforskel VA - VB)
     \     /
     R2   Rx (Sensor)
      \   /
       GND
```

### Formel for differentiel spænding ($V_G$):
$$V_G = V_A - V_B = V_{in} \cdot \left( \frac{R_2}{R_1 + R_2} - \frac{R_x}{R_3 + R_x} \right)$$

### Balancebetingelse:
Når broen er i balance, er spændingsforskellen $V_G = 0\text{V}$. Det betyder at:
$$\frac{R_1}{R_2} = \frac{R_3}{R_x} \implies R_x = \frac{R_3 \cdot R_2}{R_1}$$

Hvis $R_x$ (sensoren) ændrer sig bare en lille smule, kommer broen ud af balance, og $V_G$ bliver ulig 0V. Dette lille spændingssignal forstærkes typisk med en instrumentationsforstærker før det sendes til en ADC.

**Kort eksamensforklaring**:
> En Wheatstonebro sammenligner to spændingsdelere. Hvis broen er i balance, er spændingsforskellen mellem midtpunkterne 0V. Hvis sensorens modstand $R_x$ ændrer sig, opstår der en lille spændingsforskel $V_G$, som vi kan måle. Det gør det muligt at registrere mikroskopiske ændringer, som en normal spændingsdeler ikke ville have opløsning nok til at fange.

---
