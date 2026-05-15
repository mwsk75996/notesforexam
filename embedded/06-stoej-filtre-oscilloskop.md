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
