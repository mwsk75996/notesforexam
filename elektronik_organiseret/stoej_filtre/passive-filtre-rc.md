# Filtertyper

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
