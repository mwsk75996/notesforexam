# Sensorer og kalibrering

## Sensoroversigt

```text
Sensor          Måler                         Signal/interface
DHT11           temperatur + fugtighed         digital data pin
BMP280          tryk + temperatur              I2C/SPI
MQ-135          gas/luftkvalitet               analog spænding
LDR             lysniveau                      analog spænding via spændingsdeler
MPU6050/GY-521  acceleration + rotation        I2C
HMC5883L/GY-271 magnetfelt/kompas              I2C
ADS1115         ekstern analog måling          I2C
DS18B20         temperatur                     OneWire digital bus
```

God eksamensvinkel:

> Først forklarer jeg hvad sensoren fysisk måler. Derefter forklarer jeg hvilket signal ESP32 modtager, fx analog spænding, I2C-data eller OneWire-data. Til sidst forklarer jeg hvordan rå data bliver til en brugbar værdi i koden.

## DHT11

DHT11 måler:

- Temperatur
- Fugtighed

Den er simpel, men ikke super præcis. God til basisopgaver.

Vigtigt:

- Kræver typisk et library.
- Data kommer digitalt, ikke som analog ADC-værdi.
- Målinger bør ikke læses alt for hurtigt efter hinanden.

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

God forklaring:

> BMP280 sender målinger digitalt over I2C/SPI. ESP32 læser altså ikke en analog spænding her; den kommunikerer med sensoren og får talværdier tilbage fra sensorens interne elektronik.

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

God forklaring:

> En LDR giver ikke selv et færdigt digitalt tal. Den ændrer modstand, og sammen med en fast modstand laver den en spændingsdeler. ESP32 læser spændingen som en ADC-værdi.

## DS18B20

DS18B20 er en digital temperatur-sensor.

Fra `ass62network`:

- Bruges med `OneWire`.
- Bruges ofte sammen med `DallasTemperature` library.
- Kan sende temperatur videre via MQTT, fx topic `esp32/temp`.

Typisk include:

```cpp
#include <OneWire.h>
#include <DallasTemperature.h>
```

Typisk setup:

```cpp
#define ONE_WIRE_PIN 19

OneWire oneWire(ONE_WIRE_PIN);
DallasTemperature sensors(&oneWire);

void setup() {
    Serial.begin(115200);
    sensors.begin();
}
```

Læs temperatur:

```cpp
sensors.requestTemperatures();
float tempC = sensors.getTempCByIndex(0);

if (tempC == DEVICE_DISCONNECTED_C) {
    Serial.println("sensor ikke fundet");
} else {
    Serial.println(tempC);
}
```

Vigtigt:

- DS18B20 bruger digital bus, ikke ADC.
- `-127` betyder ofte at sensoren ikke blev fundet.
- OneWire kræver normalt pull-up modstand på datalinjen.
- GND skal være fælles med ESP32.

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
    Serial.println("bevægelse registreret");
}
```

Vigtigt:

- Accelerometer måler acceleration på akser.
- Gyroskop måler rotation.
- Sensoren kan støje, så thresholds bør testes praktisk.
- Hvis sensoren sidder skævt, skal det tænkes med i kalibreringen.

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
