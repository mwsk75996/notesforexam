# Sensorer og kalibrering

## DHT11

DHT11 måler:

- Temperatur
- Fugtighed

Den er simpel, men ikke super præcis. God til basisopgaver.

Typisk brug:

```text
Indeklima
Komfort-score
Fugtighedsovervågning
```

## BMP280

BMP280 måler:

- Lufttryk
- Temperatur

Tryk kan bruges til at estimere højde.

Fra opgaverne:

```text
Højere tryk  -> typisk lavere højde
Lavere tryk  -> typisk højere højde
```

Temperatur kan påvirke højdemålingen, fordi luftens densitet ændrer sig.

## MQ-135

MQ-135 bruges som gassensor/luftkvalitetssensor.

Vigtigt:

- Sensoren har en heater.
- Den skal varme op før målingen er stabil.
- I opgaven blev der brugt cirka `30 sekunder` warm-up.

Eksempel:

```cpp
delay(30000); // MQ-135 warm-up
```

Thresholds fra Nordic Fresh Air:

```text
ADC < 200       = god luftkvalitet
ADC 200-250     = moderat luftkvalitet
ADC > 250       = dårlig luftkvalitet
```

LED-eksempel:

```text
Grøn LED  = god luft
Gul LED   = moderat luft
Rød LED   = dårlig luft, evt. blink
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

## GY-521 / MPU6050

GY-521 har:

- Accelerometer
- Gyroskop
- Temperaturmåling

Bruges til:

- Bevægelse
- Tilt
- Rotation
- Step counter
- Alarm ved hældning

Typisk logik:

```cpp
if (abs(accelX) > threshold || abs(accelY) > threshold) {
    Serial.println("bevaegelse registreret");
}
```

## HMC5883L / GY-271

Kompas/magnetometer måler magnetfelt i:

```text
X, Y, Z
```

Det kan bruges til heading/retning:

```text
Nord, Syd, Øst, Vest osv.
```

Fejlkilder:

- Magnetisk interferens
- Metal tæt på sensoren
- Dårlig kalibrering
- Sensoren ligger skævt

## ADS1115

ADS1115 er en ekstern ADC.

Fordel:

- Højere opløsning end ESP32 ADC
- Mere stabile målinger
- God til små analoge signaler

Fra opgaverne blev der set rå værdier omkring `2293-2299` og cirka `0.287V`.

## Kalibrering

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

God eksamensforklaring:

> Thresholds er ikke universelle. De afhænger af sensor, miljø, ledninger, spænding og placering. Derfor tester man rå værdier først og vælger grænser ud fra konkrete målinger.
