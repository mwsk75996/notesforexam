# Decoupling kondensator

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
