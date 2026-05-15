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

## Praktisk rover-strøm

Fra jeres batteri/display-opgave:

- Brug fælles GND.
- Brug sikring på batteriet, fx `3-5A`.
- Brug main switch.
- Brug kondensatorer på output, fx `1000 uF`.
- Servoer/motorer bør ikke drives direkte fra ESP32.
- ESP32 skal have stabil `3.3V` eller passende `VIN/5V`, afhængigt af board.
- Flere LiPo i parallel kræver samme spænding før de kobles sammen, fx indenfor `+-0.05V`.
