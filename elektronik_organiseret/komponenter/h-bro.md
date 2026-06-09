# Motorstyring (H-bro og Torque)

### H-bro (H-Bridge)
En H-bro bruges til at styre en DC-motors rotationsretning ved at vende polariteten på spændingen over motoren. Den består af 4 transistorer (switches) tegnet som et H:

```text
         VCC
        /   \
      S1     S3
      /  Motor\
     +---( M )---+
     \           /
      S2       S4
        \     /
          GND
```

- **Fremad**: Tænd **S1 og S4** (strømmen løber fra venstre mod højre).
- **Bagud**: Tænd **S3 og S2** (strømmen løber fra højre mod venstre).
- **Brems**: Tænd **S2 og S4** (kortslutter motoren til GND, hvilket genererer elektromagnetisk modstand).
- **Kortslutningsfare (Shoot-through)**: Hvis S1 og S2 (eller S3 og S4) tændes samtidigt, opstår en direkte kortslutning mellem VCC og GND, hvilket omgående ødelægger transistorerne!

### Torque (Drejningsmoment) og effektberegning
- **Moment ($T$ eller $\tau$)**: Kraft gange arm. Måles i Newtonmeter ($\text{Nm}$).
  $$T = F \cdot r$$
  Hvor $F$ er kraften i Newton ($\text{N}$) og $r$ er radius/armen i meter ($\text{m}$).
- **Sammenhæng mellem effekt ($P$) og moment ($T$)**:
  $$P = T \cdot \omega$$
  Hvor $P$ er mekanisk effekt i Watt ($\text{W}$), og $\omega$ er vinkelhastigheden i radianer pr. sekund ($\text{rad/s}$).
  Vinkelhastigheden findes ud fra rotationshastigheden $n$ i RPM (omdrejninger pr. minut):
  $$\omega = \frac{2\pi \cdot n}{60}$$
- **DC-motor karakteristik**:
  - Momentet er direkte proportionalt med strømmen: $T = K_t \cdot I$
  - Rotationshastigheden er proportional med spændingen: $U \approx K_e \cdot \omega$
  - Ved høj belastning (højt moment) trækker motoren meget strøm. Hvis motoren blokeres (stall torque), trækker den maksimal strøm, hvilket kan brænde motoren eller driveren af (brownout/overload).
