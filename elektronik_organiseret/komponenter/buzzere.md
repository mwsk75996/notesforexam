# Buzzere: Aktiv vs. Passiv

En buzzer bruges til at lave lydsignaler (alarmer):
- **Aktiv buzzer**: Har en indbygget oscillator. Når du tilslutter en DC-spænding (fx 3.3V til en GPIO pin), begynder den straks at hyle med en fast frekvens (typisk 2.5 kHz). Styres simpelt med `digitalWrite(pin, HIGH)`.
- **Passiv buzzer**: Har ingen indbygget oscillator – det er blot en piezo-skive. Den kræver et AC-signal (fx en firkantbølge / PWM) for at svinge og lave lyd. Ved at ændre PWM-frekvensen kan du generere forskellige toner og spille melodier. Styres på ESP32 med `ledcWriteTone()`.
