# Multimeter og målinger

Brug multimeteret til at kontrollere dit kredsløb:
- **Måle spænding (V)**: Måles **parallelt** over den komponent, du vil kende spændingsfaldet over. Kredsløbet skal være tændt.
- **Måle strøm (A)**: Måles **i serie**. Du skal afbryde kredsløbet og lade strømmen løbe igennem multimeteret.
- **Måle modstand ($\Omega$)**: Måles over komponenten **uden strøm** på kredsløbet (afbryd strømkilden helt, ellers ødelægges målingen eller multimeteret).
- **Kontinuitetstest (Bip)**: Bruges til at tjekke for uønskede kortslutninger eller bekræfte, at der er elektrisk forbindelse (fx at GND er fælles i hele kredsløbet).

**Vigtig eksamensforklaring**:
> Ohms lov bruges til at finde den manglende værdi i kredsløbet. Hvis jeg kender spænding og strøm, kan jeg finde modstanden. Effektformlen bruges bagefter til at se, hvor meget energi komponenten afsætter som varme, så vi sikrer, at modstandens watt-rating (fx 0.25W) ikke overskrides.


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
