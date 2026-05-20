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
