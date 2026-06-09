# Støj, filtre og oscilloskop

Støj er uønskede udsving i et signal.

Det kan komme fra:

- Lange ledninger
- Dårlig GND
- Motorer og servoer
- ESP32/WiFi
- Dårlig strømforsyning
- Sensorer der naturligt varierer

## Filtertyper

### Low-pass filter

Lader lave frekvenser passere og dæmper hurtige ændringer.

God til:

- Temperaturmålinger
- Langsomt skiftende sensorsignaler
- Glatning af støj

Eksempel fra opgave:

```text
Støjfyldt temperatursignal -> low-pass filter
```

### High-pass filter

Lader hurtige ændringer passere og dæmper langsomme/statiske signaler.

God til:

- Bevægelsessensorer
- Pludselige ændringer
- Fjerne DC-offset

Eksempel fra opgave:

```text
Bevægelsessensor der skal reagere hurtigt -> high-pass filter
```

### Band-pass filter

Lader kun et bestemt frekvensområde passere.

God til:

- Radio
- Bestemt signalbånd

Eksempel:

```text
Radiosystem der kun skal modtage ét frekvensbånd -> band-pass filter
```

### Band-stop / notch filter

Fjerner et bestemt frekvensområde.

God til:

- 50Hz brum fra strømnet

Eksempel:

```text
Mikrofon med 50Hz brum -> band-stop filter
```

## Passivt filter

Et passivt filter bruger fx:

- Modstand
- Kondensator
- Spole

Eksempel:

```text
100 nF kondensator mellem VCC og GND tæt på sensoren
```

Det bruges til at dæmpe støj på forsyningen.

## RC low-pass filter

Et simpelt low-pass filter kan laves med en modstand og en kondensator.

```text
sensor signal --- R --- ESP32 ADC
                  |
                  C
                  |
                 GND
```

Cutoff-frekvensen kan beregnes med:

```text
fc = 1 / (2 * pi * R * C)
```

Eksempel:

```text
R = 10 kOhm
C = 100 nF

fc = 1 / (2 * pi * 10000 * 0.0000001)
fc = cirka 159 Hz
```

Det betyder at langsomme ændringer under cirka `159 Hz` slipper bedre igennem, mens hurtige udsving/støj dæmpes.

God forklaring:

> Et RC low-pass filter gør signalet mere roligt, fordi kondensatoren modarbejder hurtige spændingsændringer. Det er nyttigt til langsomme sensorer, men dårligt hvis man skal måle hurtige pulser.

## Hvor sætter man filteret?

To typiske steder:

1. På forsyningen

```text
VCC --- sensor
 |
100 nF
 |
GND
```

2. På signalledningen

```text
sensor output -> filter -> ESP32 GPIO
```

Forsyningsfilter hjælper hvis strømmen er ustabil. Signalfilter hjælper hvis selve målingen hopper.

## Decoupling kondensator

En decoupling kondensator sættes typisk mellem `VCC` og `GND` tæt på en sensor eller IC.

Typisk værdi:

```text
100 nF keramisk kondensator tæt på komponenten
```

Den hjælper med korte, hurtige strømspidser.

Eksempel:

```text
3.3V ---- sensor VCC
  |
100 nF
  |
GND ---- sensor GND
```

Større kondensatorer, fx `470 uF` eller `1000 uF`, bruges mere som buffer på forsyningen ved motorer, servoer eller lange ledninger.

Kort forskel:

```text
100 nF      -> hurtig højfrekvent støj tæt på IC/sensor
470-1000 uF -> større spændingsdyk på forsyningen
```

## Oscilloskop

Oscilloskop bruges til at se signaler over tid.

Man kan se:

- Spændingsniveau
- Støj
- PWM duty cycle
- Frekvens
- Pulsbredde
- Om signalet er stabilt

Hvis oscilloskopet har FFT, kan man se frekvensindholdet.

Eksempel fra opgave:

```text
Mål sensorens output pin
Se om signalet hopper
Brug FFT til at finde støjfrekvens
```

God eksamensforklaring:

> Serial monitor viser tal efter ADC-konvertering, men et oscilloskop viser det elektriske signal direkte. Derfor er oscilloskopet bedre til at se støj, timing og PWM.

## PWM på oscilloskop

PWM ser ud som et firkantsignal.

```text
HIGH  ____      ____      ____
     |    |    |    |    |    |
LOW _|    |____|    |____|    |____
```

Det man typisk måler:

- Frekvens: hvor ofte signalet gentager sig.
- Periode: tiden for én hel cyklus.
- Duty cycle: hvor stor del af perioden signalet er HIGH.
- Amplitude: spændingsniveau, fx `0V` til `3.3V`.

Eksempel:

```text
Periode = 1 ms
HIGH tid = 0.25 ms

duty cycle = 0.25 / 1.0 = 25%
frekvens = 1 / 0.001 = 1000 Hz
```

Hvis duty cycle ændres fra `25%` til `75%`, bliver HIGH-tiden længere, men spændingsniveauet er stadig typisk `0V` eller `3.3V`.

## Software filter

Man kan også filtrere i kode.

Simpelt gennemsnit:

```cpp
int sum = 0;

for (int i = 0; i < 10; i++) {
    sum += analogRead(34);
    delay(5);
}

int average = sum / 10;
```

Fordel:

- Nemt at lave
- Kræver ingen ekstra komponenter

Ulempe:

- Fjerner ikke elektrisk støj før ADC
- Kan gøre systemet langsommere

## Glidende filter

Et glidende filter kan gøre værdien roligere uden at gemme mange målinger.

```cpp
float filtered = 0;

void loop() {
    int raw = analogRead(34);
    filtered = 0.9 * filtered + 0.1 * raw;

    Serial.println(filtered);
    delay(50);
}
```

Her betyder `0.9` at den gamle værdi vægter meget, og `0.1` at den nye måling kun påvirker lidt.

Fordel:

- Roligere sensorværdi.
- Simpelt at skrive.
- Kræver ikke ekstra komponenter.

Ulempe:

- Reagerer langsommere på rigtige ændringer.
- Fjerner ikke støj før signalet rammer ADC'en.

God eksamensforklaring:
> Hardwarefiltre forbedrer det elektriske signal før målingen. Softwarefiltre glatter tallene efter målingen. Hvis støjen er kraftig nok til at forstyrre ADC'en, er software alene ikke altid nok.

---

## Avanceret softwarefilter: Kalman-filter
I emneoversigten nævnes Kalman-filteret under filtrering og sensor-fusion:
- **Hvad er det**: En matematisk algoritme, der estimerer den sande tilstand af et system ud fra en række støjfyldte målinger over tid.
- **Anvendelse**: Typisk til sensor-fusion, fx i droner eller balance-robotter. Her kombinerer man accelerometer-data (som reagerer hurtigt, men er støjfyldte pga. vibrationer) med gyroskop-data (som er rolige på kort sigt, men driver/drifter over tid). Kalman-filteret vægter de to sensorer optimalt for at beregne den præcise vinkel.
- **Konceptuelt flow (rekursivt)**:
  1. **Predict (Forudsig)**: Estimer den næste tilstand ud fra en fysisk model af systemet.
  2. **Update (Opdater)**: Mål med sensorerne, beregn usikkerheden (Kalman Gain), og korriger forudsigelsen med målingen.

---

## Værktøjer til Elektronik og Udvikling

### Breadboards (Hulprint)
- **Opbygning**: Bruges til hurtig prototype-bygning uden lodning.
  - **Yderbaner (Power rails)**: Kører lodret (eller vandret i toppen/bunden) langs hele brættet. Bruges til VCC ($3.3\text{V}/5\text{V}$) og GND.
  - **Inderbaner**: Forbundet i grupper af 5 huller på tværs (vinkelret på power rails).
  - **Midterdelingen**: Adskiller de to sider og passer præcist til bredden på IC'er og ESP32, så benene på hver side ikke kortsluttes.

### Lodning (Soldering)
- **Tips & Tricks**:
  - **Rengøring**: Hold loddekolbens spids ren med messinguld eller en fugtig svamp.
  - **Fortinning (Tinning)**: Kom altid en smule frisk tin på spidsen før lodning. Det forbedrer varmeoverførslen og beskytter spidsen mod oxidation.
  - **Teknik**: Varm både komponentbenet og kobberbanen på printkortet op samtidigt med kolben i 2-3 sekunder. Tilfør derefter tin til **samlingen** (ikke direkte på kolbespidsen), lad tinnet flyde ud, fjern tinnet, og fjern til sidst kolben. Hold samlingen helt stille, til tinnet er størknet.
  - **Kold lodning (Cold joint)**: Opstår hvis samlingen ikke blev varm nok, eller hvis komponenten flyttede sig under afkøling. Kendetegnes ved en mat, grålig, ru eller kugleformet overflade. Giver dårlig elektrisk forbindelse og knækker nemt mekanisk.

### Falstad
Falstad er en interaktiv, web-baseret kredsløbssimulator. Den er fremragende til at tegne kredsløb og visualisere strømmens retning (animerede prikker) og spændinger (farver) over tid. God til at teste spændingsdelere, filtre og 555-timere virtuelt, før man bygger dem i virkeligheden.

### KiCad Design-workflow
KiCad er det softwareprogram, I skal bruge til at designe kredsløb og PCB'er (printkort). Flowet består af:
1. **Schematic Editor (Eeschema - Diagramtegning)**:
   - Placer symboler for dine komponenter (fx ESP32, MQ-135, OLED).
   - Forbind komponenternes ben med ledninger (Wires) eller Net Labels.
   - Kør **ERC (Electrical Rules Check)** for at sikre, at der ikke er uforbundne pins, glemte strømforsyninger eller direkte kortslutninger.
2. **Footprint Association (Komponent-kobling)**:
   - Forbind hvert skematisk symbol med et fysisk footprint (layout-pakke, fx en $0.25\text{W}$ modstand eller et 38-pin DIP-modul).
3. **PCB Editor (Pcbnew - Boardlayout)**:
   - Definer printkortets fysiske form (Edge.Cuts-laget).
   - Placer komponenternes footprints hensigtsmæssigt.
   - Forbind komponenterne med kobberbaner (Tracks) på top- og bundlag (F.Cu / B.Cu).
   - Opret **Ground Planes (Copper Fills)** til GND for at reducere elektrisk støj.
   - Kør **DRC (Design Rules Check)** for at verificere, at banerne ikke ligger for tæt, er for tynde til strømmen, eller overtræder fabrikationsgrænserne.

### Funktionsgenerator
- **Hvad er det**: Et laboratorieapparat, der genererer elektriske spændingsbølger med kontrolleret frekvens, form og amplitude.
- **Waveforms (Bølgeformer)**:
  - **Sinusbølge**: Blød, harmonisk svingning. Bruges ofte til lyd- og radiotests.
  - **Firkantbølge**: Skifter øjeblikkeligt mellem to niveauer (HIGH/LOW). Bruges til clock-signaler og digitale kredsløb.
  - **Pulsbølge**: En firkantbølge, hvor bredden af pulsen (duty cycle) kan justeres uafhængigt.
  - **Trekantbølge**: Stiger og falder helt lineært. Bruges til analoge sweep-kredsløb.
  - **Savtandsbølge**: Stiger lineært og falder stejlt lodret (eller omvendt).
- **Parametre**:
  - `Frekvens`: Antal svingninger pr. sekund (Hz).
  - `Amplitude`: Spændingshøjden målt Peak-to-Peak ($V_{pp}$), fx fra $-5\text{V}$ til $+5\text{V}$ ($10V_{pp}$).
  - `DC Offset`: Lægger en konstant jævnspænding under signalet, så det fx flyttes op i det positive område ($0-3.3\text{V}$ i stedet for $-1.65\text{V}$ til $+1.65\text{V}$).
