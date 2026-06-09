# Software filter

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


## Simpelt gennemsnit

```cpp
int readAverage(int pin) {
    int sum = 0;

    for (int i = 0; i < 10; i++) {
        sum += analogRead(pin);
        delay(5);
    }

    return sum / 10;
}
```
