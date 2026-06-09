# Kalibrering

Kalibrering betyder at man finder de rigtige grænser ud fra rigtige målinger.

God proces:

1. Print rå sensorværdi i serial monitor.
2. Test i flere situationer.
3. Noter typiske minimum/maksimum.
4. Vælg thresholds.
5. Test igen og juster.

Eksempel:

```cpp
Serial.print("gas=");
Serial.print(gasValue);
Serial.print(" light=");
Serial.println(lightValue);
```


## Eksempel på threshold ud fra målinger

Hvis en LDR giver disse rå værdier:

```text
mørkt rum:        700-1100
normal belysning: 1800-2400
stærkt lys:       3000-3600
```

Så kan man vælge:

```text
under 1500  -> for mørkt
1500-2800   -> normal belysning
over 2800   -> stærkt lys
```

Kode:

```cpp
int light = analogRead(34);

if (light < 1500) {
    Serial.println("for mørkt");
} else if (light > 2800) {
    Serial.println("stærkt lys");
} else {
    Serial.println("normal belysning");
}
```

Det vigtige er ikke selve tallene, men metoden: mål først, vælg thresholds bagefter.


## Fejlkilder ved sensorer

Typiske årsager til dårlige målinger:

- Sensoren får forkert spænding.
- GND er ikke fælles.
- Analog pin flyder.
- Ledninger er for lange.
- Motorer eller WiFi laver støj.
- Sensoren er ikke varmet op.
- Forkert I2C-adresse.
- SDA/SCL er byttet rundt.
- Thresholds er kopieret fra et andet setup uden ny kalibrering.

God eksamensforklaring:

> Thresholds er ikke universelle. De afhænger af sensor, miljø, ledninger, spænding og placering. Derfor tester man rå værdier først og vælger grænser ud fra konkrete målinger.
