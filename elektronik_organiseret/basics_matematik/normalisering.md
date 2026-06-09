# Normalisering

Normalisering betyder at man laver forskellige målinger om til samme skala, fx `0-100`.

Eksempel:

```cpp
int normalize(float value, float minValue, float maxValue) {
    float normalized = (value - minValue) * 100.0 / (maxValue - minValue);
    return constrain(normalized, 0, 100);
}
```

Det er nyttigt når man vil kombinere flere sensorer til én score.

Eksempel fra indeklima:

```text
DHT11 temperatur
BMP280 temperatur
Fugtighed
Tryk

-> normaliseres
-> vægtes
-> komfort-score
```


## Normalisering 0-100

```cpp
int normalize(float value, float minValue, float maxValue) {
    float normalized = (value - minValue) * 100.0 / (maxValue - minValue);
    return constrain(normalized, 0, 100);
}
```
