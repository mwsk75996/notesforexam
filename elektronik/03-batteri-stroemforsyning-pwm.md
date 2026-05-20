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

## Praktisk rover-strøm

Fra jeres batteri/display-opgave:

- Brug fælles GND.
- Brug sikring på batteriet, fx `3-5A`.
- Brug main switch.
- Brug kondensatorer på output, fx `1000 uF`.
- Servoer/motorer bør ikke drives direkte fra ESP32.
- ESP32 skal have stabil `3.3V` eller passende `VIN/5V`, afhængigt af board.
- Flere LiPo i parallel kræver samme spænding før de kobles sammen, fx indenfor `+-0.05V`.
