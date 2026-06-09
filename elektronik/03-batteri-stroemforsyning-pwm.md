# Batteri, strømforsyning og PWM

## LiPo batteri

Et 1S LiPo batteri har typisk:

```text
Nominel spænding: 3.7V
Fuldt opladet:    4.2V
Næsten tomt:      3.0V
```

Man skal ikke aflade et LiPo for langt ned, da det kan skade batteriet.

## Oplader modul

Typisk LiPo charger-modul:

- `5V` input
- `BAT+` og `BAT-` til batteriet
- Rød LED betyder oplader
- Blå LED betyder fuldt opladet
- Stopper automatisk når batteriet er fuldt

## Driftstid

Simpel formel:

```text
driftstid i timer = kapacitet i mAh / strømforbrug i mA
```

Eksempel:

```text
Batteri = 2000 mAh
Forbrug = 500 mA

driftstid = 2000 / 500 = 4 timer
```

I praksis bliver det ofte lidt mindre på grund af tab i regulatorer og varierende strømforbrug.

Vigtigt:

> mAh alene fortæller ikke hele historien. Et batteri med høj kapacitet kan stadig være dårligt valg, hvis det ikke kan levere nok strøm til motorer, servoer og ESP32 samtidig.

## Boost og buck converter

En boost converter hæver spændingen.

```text
3.7V batteri -> 5V output
```

En buck converter sænker spændingen.

```text
12V input -> 5V output
```

Effektivitet er typisk ikke 100%. Hvis en converter er 85-90% effektiv, skal batteriet levere mere effekt end outputtet bruger.

```text
P = U * I
```

Hvis output er:

```text
5V * 1A = 5W
```

Så skal batterisiden levere lidt mere end `5W`, fordi der er tab i converteren.

Eksempel med effektivitet:

```text
Output: 5V * 1A = 5W
Effektivitet: 85%

Input-effekt = 5W / 0.85 = 5.88W
```

Hvis batteriet er cirka `3.7V`:

```text
Input-strøm = 5.88W / 3.7V = 1.59A
```

Det betyder at en 5V converter der leverer `1A` ud, kan trække omkring `1.6A` fra et 1S LiPo batteri.

## Motorer, servoer og brownout

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

## PWM

PWM tænder og slukker hurtigt for et signal. Duty cycle bestemmer hvor stor en del af tiden signalet er tændt.

```text
0% duty cycle   = altid slukket
50% duty cycle  = tændt halvdelen af tiden
100% duty cycle = altid tændt
```

Bruges til:

- LED brightness
- Motorhastighed
- Servo-styring
- Buzzer/tones

Eksempel:

```cpp
analogWrite(ledPin, 128); // cirka 50% på 8-bit PWM
```

På ESP32 bruges ofte `ledc`:

```cpp
ledcAttachPin(26, 0);
ledcSetup(0, 5000, 8);
ledcWrite(0, 128);
```

God forklaring:

> PWM ændrer ikke selve spændingen direkte. Den ændrer hvor længe signalet er tændt og slukket. Gennemsnittet opleves som lavere effekt, for eksempel en LED der lyser svagere.

## PWM frekvens og duty cycle

PWM har to vigtige begreber:

```text
Frekvens    = hvor hurtigt signalet tænder/slukker
Duty cycle  = hvor stor del af perioden signalet er HIGH
```

Eksempel:

```text
Frekvens = 1000 Hz
Periode = 1 ms
Duty cycle = 25%

Signalet er HIGH i 0.25 ms og LOW i 0.75 ms
```

Til LED bruges frekvensen ofte høj nok til at øjet ikke ser blink.

Til motorer bruges PWM til at regulere gennemsnitlig effekt, men for lav frekvens kan give hørbar summen.

Til servoer er signalet anderledes end almindelig LED-PWM. Mange hobbyservoer styres typisk med pulser omkring:

```text
50 Hz
1.0 ms pulse  -> én yderposition
1.5 ms pulse  -> midtposition
2.0 ms pulse  -> anden yderposition
```

## Praktisk rover-strøm og batteriopbygning

Fra jeres batteri/display-opgave:
- Brug fælles GND.
- Brug sikring på batteriet, fx `3-5A`.
- Brug main switch.
- Brug kondensatorer på output, fx `1000 uF`.
- Servoer/motorer bør ikke drives direkte fra ESP32.
- ESP32 skal have stabil `3.3V` eller passende `VIN/5V`, afhængigt af board.

### Batterikombinationer
- **Serieforbindelse (Series)**: Spændingen lægges sammen, kapaciteten er uændret.
  $$U_{total} = U_1 + U_2 + \dots, \quad Capacity_{total} = Capacity_{1}$$
  *Eksempel*: To $3.7\text{V}$ $2000\text{mAh}$ celler i serie (2S) giver $7.4\text{V}$ og $2000\text{mAh}$.
- **Parallelforbindelse (Parallel)**: Kapaciteten lægges sammen, spændingen er uændret.
  $$Capacity_{total} = Capacity_1 + Capacity_2 + \dots, \quad U_{total} = U_1$$
  *Eksempel*: To $3.7\text{V}$ $2000\text{mAh}$ celler i parallel (1S2P) giver $3.7\text{V}$ og $4000\text{mAh}$.
  *VIGTIGT*: Batterierne skal have nøjagtig samme spænding (indenfor $\pm0.05\text{V}$) inden de kobles sammen for at undgå enorme udligningsstrømme og brandfare.

---

## Dioder og Transistorer

### Dioder (Ensrettere)
Dioder tillader kun strøm at løbe i én retning (fra Anode [+] til Katode [-], markeret med en ring på komponenten).
- **Spændingsfald ($U_f$)**: Når dioden leder, falder der en spænding over den.
  - Almindelig Silicium-diode (fx 1N4007): $\approx 0.7\text{V}$
  - Schottky-diode (hurtigere, lavere tab): $\approx 0.3\text{V}$ (bruges ofte til ensretning og beskyttelse mod forkert polaritet).
  - LED (Lysdiode): Typisk $1.8\text{V}$ (rød) til $3.3\text{V}$ (blå/hvid). Kræver altid en seriemodstand for at begrænse strømmen.
  - Zener-diode: Designet til at lede "baglæns" (breakdown) ved en meget præcis spænding. Bruges til spændingsregulering og beskyttelse.

### Transistorer (BJT og MOSFET)
Transistorer fungerer som elektroniske kontakter eller forstærkere.

1. **BJT (Bipolar Junction Transistor)**:
   - **Styring**: Strømstyret. En lille strøm på Basen ($I_B$) styrer en stor strøm mellem Collector ($C$) og Emitter ($E$).
     $$I_C = \beta \cdot I_B$$
   - **Typer**: **NPN** (tænder ved HIGH spænding på base i forhold til emitter) og **PNP** (tænder ved LOW spænding).
   - **Ben**: Base (B), Collector (C), Emitter (E).

2. **MOSFET (Field-Effect Transistor)**:
   - **Styring**: Spændingsstyret. Spændingen mellem Gate og Source ($U_{GS}$) styrer modstanden ($R_{DS(on)}$) mellem Drain ($D$) og Source ($S$). Da Gate er isoleret, løber der stort set ingen strøm ind i Gate (høj indgangsimpedans).
   - **Typer**: **N-channel** (tænder når $U_{GS} > U_{threshold}$ - typisk HIGH logik) og **P-channel** (tænder når $U_{GS} < 0$ - typisk LOW logik).
   - **Ben**: Gate (G), Drain (D), Source (S).
   - *MOSFET er ideel som switch til høje strømme (fx motorstyring), fordi dens tændte modstand ($R_{DS(on)}$) er ekstremt lav, hvilket minimerer varmeafgivelse.*

---

## Motorstyring (H-bro og Torque)

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
