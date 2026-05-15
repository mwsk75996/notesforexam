# Spændingsdeler, Wheatstonebro og Thevenin

## Spændingsdeler

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

## LDR som spændingsdeler

En LDR ændrer modstand efter lys.

Typisk setup:

```text
3.3V -- LDR -- GPIO analog input -- 10k -- GND
```

Når lyset stiger, falder LDR-modstanden. I jeres Nordic Fresh Air-opgave gav det højere ADC-værdi ved mere lys.

Eksempel:

```cpp
int light = analogRead(34);

if (light < 2500) {
    // for lavt lysniveau
}
```

## Wheatstonebro

En Wheatstonebro bruges til at måle små ændringer i modstand.

Den består af to spændingsdelere ved siden af hinanden. Man måler forskellen mellem midtpunkterne.

Den bruges typisk til:

- Strain gauges
- Vægt/load cells
- Små sensorændringer
- Præcise modstandsmålinger

God forklaring:

> En Wheatstonebro sammenligner to spændingsdelere. Hvis broen er i balance, er spændingsforskellen mellem midtpunkterne 0V. Hvis en modstand ændrer sig, opstår der en spændingsforskel, som kan måles.

## Thevenin

Thevenin bruges til at forenkle et større kredsløb til én spændingskilde og én seriemodstand.

```text
Stort kredsløb -> Vth + Rth
```

Fremgangsmåde:

1. Fjern load-modstanden.
2. Find åben-kreds-spændingen. Det er `Vth`.
3. Sluk uafhængige kilder for at finde `Rth`.
4. Tegn kredsløbet som `Vth` i serie med `Rth` og load.

Når man slukker kilder:

- Ideel spændingskilde bliver til kortslutning.
- Ideel strømkilde bliver til åben forbindelse.

God eksamensforklaring:

> Thevenin gør det nemmere at regne på en load. I stedet for at regne på hele kredsløbet hver gang, laver man en ækvivalent spændingskilde med en intern modstand.
