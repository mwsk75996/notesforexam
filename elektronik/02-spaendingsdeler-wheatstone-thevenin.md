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

## Thevenin eksempel

Forestil dig dette kredsløb:

```text
12V -- R1 1k -- punkt A -- R2 2k -- GND
                  |
                  +-- RL 3k -- GND
```

`RL` er load-modstanden. Det kan fx være en sensor, en LED-del eller et andet kredsløb der er koblet på punkt A.

Målet er at forenkle alt til venstre for `RL`, så loaden kun ser:

```text
Vth -- Rth -- RL -- GND
```

### 1. Fjern loaden

Først fjerner vi `RL`, så punkt A er åben.

```text
12V -- R1 1k -- punkt A -- R2 2k -- GND
```

Nu er kredsløbet bare en spændingsdeler.

### 2. Find Vth

`Vth` er spændingen på punkt A uden load.

```text
Vth = Vin * R2 / (R1 + R2)
Vth = 12V * 2k / (1k + 2k)
Vth = 12V * 2 / 3
Vth = 8V
```

Så Thevenin-spændingen er:

```text
Vth = 8V
```

### 3. Find Rth

Nu skal vi finde modstanden set ind i punkt A.

Vi slukker spændingskilden. En ideel spændingskilde bliver til en kortslutning.

Det betyder at `12V` bliver til `GND`.

```text
GND -- R1 1k -- punkt A -- R2 2k -- GND
```

Set fra punkt A går både `R1` og `R2` til GND. De ligger derfor parallelt.

```text
Rth = R1 || R2
Rth = (R1 * R2) / (R1 + R2)
Rth = (1k * 2k) / (1k + 2k)
Rth = 2000k / 3k
Rth = 0.667k
Rth = 667 Ohm
```

Så Thevenin-modstanden er:

```text
Rth = 667 Ohm
```

### 4. Tegn det forenklede kredsløb

Nu kan hele kredsløbet til venstre for `RL` erstattes med:

```text
8V -- Rth 667 Ohm -- RL 3k -- GND
```

Det er meget nemmere at regne på.

### 5. Beregn spændingen over loaden

Nu er `Rth` og `RL` bare en ny spændingsdeler.

```text
V_RL = Vth * RL / (Rth + RL)
V_RL = 8V * 3000 / (667 + 3000)
V_RL = 8V * 3000 / 3667
V_RL = 6.54V
```

Så når loaden sættes på, falder spændingen fra `8V` til cirka `6.54V`.

Det er pointen med Thevenin: uden load ser punkt A ud som `8V`, men når loaden trækker strøm, falder spændingen på grund af den interne Thevenin-modstand.

Kort eksamenssvar:

> Først fjerner jeg loaden og finder åben-kreds-spændingen som `Vth`. Derefter slukker jeg spændingskilden og finder modstanden set fra loadens terminaler som `Rth`. Til sidst erstatter jeg hele kredsløbet med en spændingskilde og en seriemodstand, så det er nemmere at beregne load-spænding og load-strøm.

God eksamensforklaring:

> Thevenin gør det nemmere at regne på en load. I stedet for at regne på hele kredsløbet hver gang, laver man en ækvivalent spændingskilde med en intern modstand.
