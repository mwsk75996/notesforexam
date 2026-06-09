# Motorer, servoer og brownout

Motorer og servoer bruger ofte meget mere strøm end ESP32.

Typisk problem:

```text
Motor starter -> strømforbrug stiger hurtigt
Spænding falder kortvarigt
ESP32 får for lav spænding
ESP32 resetter eller opfører sig mærkeligt
```

Det kaldes ofte brownout.

Symptomer:

- ESP32 genstarter når motoren starter.
- Serial monitor viser brownout/reset.
- WiFi disconnecter når servo eller motor bevæger sig.
- Sensorværdier hopper når motorer kører.

Løsninger:

- Brug separat motor driver til motorer.
- Brug regulator der kan levere nok ampere.
- Brug fælles GND mellem ESP32, motor driver og strømforsyning.
- Sæt kondensator tæt på motor/driver, fx `470 uF` til `1000 uF`.
- Sæt `100 nF` kondensator tæt på sensor/IC for højfrekvent støj.
- Før motorstrøm udenom ESP32 boardet.

Vigtigt:

> En GPIO på ESP32 kan kun levere små mængder strøm. Den kan styre et signal til en motor driver, transistor eller MOSFET, men den må ikke drive en motor direkte.

Simpel motorstyringsidé:

```text
ESP32 GPIO/PWM -> motor driver input
batteri       -> motor driver power
motor driver  -> motor
GND fælles mellem ESP32 og motor driver
```
