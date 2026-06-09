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

## Sensor- og Aktuatorbegrebet

- **Sensor**: En transducer, der omsætter en fysisk størrelse (fx varme, tryk, lys eller gaskoncentration) til et elektrisk signal (enten en analog spænding eller digitale data). Det er et **input** til mikrokontrolleren.
- **Aktuator**: En transducer, der gør det modsatte: Omsætter et elektrisk signal til en fysisk handling (fx bevægelse, lyd eller lys). Det er et **output** fra mikrokontrolleren (fx DC-motorer, servoer, buzzere og lysdioder).

---

## Gassensorer: MQ-135 og MQ-2

Til eksamen skal I medbringe en **MQ135-MQ2** gassensor.
- **MQ-135**: Følsom over for luftkvalitet (ammoniak, benzen, alkohol, røg og $\text{CO}_2$).
- **MQ-2**: Følsom over for brændbare gasser (LPG, butan, propan, metan, brint og røg).

### Opbygning og opvarmning (Heater)
Begge sensorer virker ved hjælp af et lille varmelegeme (heater) og et halvlederlag af tindioxid ($\text{SnO}_2$).
- Når gassensoren opvarmes i ren luft, er modstanden i halvlederlaget høj ($R_0$).
- Når der er gas til stede, stiger halvlederens ledningsevne, hvilket får dens modstand ($R_s$) til at falde.
- **VIGTIGT**: Da sensoren indeholder en fysisk heater, skal den varme op for at give stabile målinger. Ved første ibrugtagning skal den køre i 24-48 timer (indbrænding). Før en måling ved eksamen skal sensoren varme op i mindst **2 minutter** (eller 30 sekunder som minimum), før data er pålidelige. Den bliver fysisk lun.

### Analog vs. Digital output på breakoutboards
De fleste MQ-breakoutboards har fire ben (VCC, GND, AOUT, DOUT):
1. **AOUT (Analog Out)**: Giver en analog spænding ($0-V_{CC}$), som stiger proportionalt med gaskoncentrationen. Læses med `analogRead()`.
2. **DOUT (Digital Out)**: Giver et digitalt HIGH/LOW signal. Modulet har en indbygget komparator og et lille potentiometer. Ved at dreje på potentiometret sætter man en threshold-grænse. Hvis gassen overskrider grænsen, skifter DOUT tilstand.

### MQ-135 kalibrering og beregning
For at få en præcis måling skal sensoren kalibreres i ren luft:
1. Mål den analoge spænding ($V_{out}$) over sensorens modstand.
2. Beregn sensorens modstand $R_s$:
   $$R_s = \frac{V_{CC} - V_{out}}{V_{out}} \cdot R_L$$
   (hvor $R_L$ er en kendt belastningsmodstand på boardet, typisk $1\text{ k}\Omega$ eller $10\text{ k}\Omega$).
3. I ren luft bestemmes referenceværdien $R_0$:
   $$R_0 = \frac{R_s}{\text{CleanAirFactor}}$$
4. Når $R_0$ er fundet og gemt i koden, kan man beregne forholdet $\frac{R_s}{R_0}$ for at udregne PPM (Parts Per Million) ud fra sensorens databladskurver.

*Thresholds fra Nordic Fresh Air (rå analoge værdier på ESP32, 0-4095)*:
- `ADC < 200` = god luftkvalitet (Grøn LED)
- `ADC 200-250` = moderat luftkvalitet (Gul LED)
- `ADC > 250` = dårlig luftkvalitet (Rød LED, evt. blink/buzzer)

---

## Barometer-typer

Et barometer måler atmosfærisk tryk. I emneoversigten nævnes følgende måleteknologier:
1. **Kviksølvsbarometer**: Klassisk fysik. Lufttrykket presser en kviksølvsøjle op i et glasrør. Meget præcist, men giftigt og stort.
2. **Aneroidbarometer**: Mekanisk. En forseglet, fleksibel metalæske (vakuumdåse) trækker sig sammen eller udvider sig ved trykændringer, hvilket flytter en viser mekanisk.
3. **Kapacitivt barometer**: Elektronisk. Trykket deformerer en fleksibel membran, som udgør den ene plade i en kondensator. Afstanden mellem pladerne ændres, hvilket ændrer kapacitansen. Strømforbruget er ekstremt lavt.
4. **Piezomodstand-barometer (Piezoresistive)**: MEMS (Micro-Electro-Mechanical Systems). Trykket bøjer en mikroskopisk siliciumpyramide, hvilket ændrer halvlederens elektriske modstand. Det er denne type, der sidder i **BMP280**-sensoren. Meget billig og udbredt.
5. **Piezoelektrisk barometer**: Genererer en elektrisk spænding direkte, når krystallen deformeres af tryk. Fungerer kun ved dynamiske (hurtigt skiftende) trykændringer.
6. **Micro-elektromagnetisk barometer**: Anvender magnetiske induktionsændringer over en mikroskopisk membran.

---

## Ultralyd vs. Time-of-Flight (ToF)

Begge sensorer bruges til afstandsmåling:

### Ultralyd (fx HC-SR04)
- **Princip**: Sender en ultralydslydbølge (Trigger) afsted og måler tiden ($t$), indtil ekkoet (Echo) vender tilbage.
- **Formel**:
  $$d = \frac{v_{lyd} \cdot t}{2}$$
  Hvor $v_{lyd} \approx 343\text{ m/s}$ ($0.0343\text{ cm/}\mu\text{s}$ ved $20^\circ\text{C}$). Division med 2 skyldes, at lyden skal rejse frem og tilbage.
- **Ulempe**: Lydbølger spreder sig kegleformet. Bløde overflader absorberer lyden, og skrå vægge kan kaste ekkoet væk, så målingen fejler.

### Time-of-Flight (ToF, fx VL53L0X)
- **Princip**: Sender en mikroskopisk, usynlig infrarød laserpuls afsted og måler tiden, det tager for lyset at blive reflekteret tilbage til sensoren.
- **Fordel**: Ekstremt præcis og måler i en snæver stråle (ikke en bred kegle). Påvirkes ikke af overfladens vinkel eller materiale i samme grad som ultralyd.
- **Ulempe**: Kan forstyrres af stærkt sollys (infrarød støj) og har kortere rækkevidde (typisk 1-2 meter).

---

## Joystick

Et joystick (som i Rover-styringen) består af:
- **X-akse og Y-akse**: To uafhængige potentiometre (spændingsdelere) monteret vinkelret på hinanden. Når joysticket bevæges, ændres modstanden, og der leveres to analoge spændinger ($0-3.3\text{V}$). Midtpunktet giver ca. $1.65\text{V}$ (ADC $\approx 2048$).
- **Z-akse (Knap)**: En indbygget taktil switch, der aktiveres, når man trykker lodret ned på joysticket. Kræver en pull-up modstand (internt i ESP32 eller eksternt), så signalet læses som `LOW` ved tryk.

---

## Buzzere: Aktiv vs. Passiv

En buzzer bruges til at lave lydsignaler (alarmer):
- **Aktiv buzzer**: Har en indbygget oscillator. Når du tilslutter en DC-spænding (fx 3.3V til en GPIO pin), begynder den straks at hyle med en fast frekvens (typisk 2.5 kHz). Styres simpelt med `digitalWrite(pin, HIGH)`.
- **Passiv buzzer**: Har ingen indbygget oscillator – det er blot en piezo-skive. Den kræver et AC-signal (fx en firkantbølge / PWM) for at svinge og lave lyd. Ved at ændre PWM-frekvensen kan du generere forskellige toner og spille melodier. Styres på ESP32 med `ledcWriteTone()`.

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
