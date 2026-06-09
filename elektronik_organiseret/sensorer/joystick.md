# Joystick

Et joystick (som i Rover-styringen) består af:
- **X-akse og Y-akse**: To uafhængige potentiometre (spændingsdelere) monteret vinkelret på hinanden. Når joysticket bevæges, ændres modstanden, og der leveres to analoge spændinger ($0-3.3\text{V}$). Midtpunktet giver ca. $1.65\text{V}$ (ADC $\approx 2048$).
- **Z-akse (Knap)**: En indbygget taktil switch, der aktiveres, når man trykker lodret ned på joysticket. Kræver en pull-up modstand (internt i ESP32 eller eksternt), så signalet læses som `LOW` ved tryk.

---
