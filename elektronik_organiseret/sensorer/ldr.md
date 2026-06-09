# LDR som spændingsdeler

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


## LDR

LDR måler lys ved at ændre modstand.

I opgaven:

```text
GPIO34 analog input
10k pulldown til GND
ADC < 2500 = for lavt lysniveau
```

Eksempel:

```cpp
int light = analogRead(34);

if (light < 2500) {
    digitalWrite(12, HIGH); // blå LED
} else {
    digitalWrite(12, LOW);
}
```

God forklaring:

> En LDR giver ikke selv et færdigt digitalt tal. Den ændrer modstand, og sammen med en fast modstand laver den en spændingsdeler. ESP32 læser spændingen som en ADC-værdi.
