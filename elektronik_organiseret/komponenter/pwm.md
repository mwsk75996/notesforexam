# PWM

PWM tænder og slukker hurtigt for et signal. Duty cycle bestemmer hvor stor en del af tiden signalet er tændt.

```text
0% duty cycle   = altid slukket
50% duty cycle  = tændt halvdelen af tiden
100% duty cycle = altid tændt
```

Bruges til:

- LED brightness
- Motorhastighed
- Servo-styring
- Buzzer/tones

Eksempel:

```cpp
analogWrite(ledPin, 128); // cirka 50% på 8-bit PWM
```

På ESP32 bruges ofte `ledc`:

```cpp
ledcAttachPin(26, 0);
ledcSetup(0, 5000, 8);
ledcWrite(0, 128);
```

God forklaring:

> PWM ændrer ikke selve spændingen direkte. Den ændrer hvor længe signalet er tændt og slukket. Gennemsnittet opleves som lavere effekt, for eksempel en LED der lyser svagere.


## PWM frekvens og duty cycle

PWM har to vigtige begreber:

```text
Frekvens    = hvor hurtigt signalet tænder/slukker
Duty cycle  = hvor stor del af perioden signalet er HIGH
```

Eksempel:

```text
Frekvens = 1000 Hz
Periode = 1 ms
Duty cycle = 25%

Signalet er HIGH i 0.25 ms og LOW i 0.75 ms
```

Til LED bruges frekvensen ofte høj nok til at øjet ikke ser blink.

Til motorer bruges PWM til at regulere gennemsnitlig effekt, men for lav frekvens kan give hørbar summen.

Til servoer er signalet anderledes end almindelig LED-PWM. Mange hobbyservoer styres typisk med pulser omkring:

```text
50 Hz
1.0 ms pulse  -> én yderposition
1.5 ms pulse  -> midtposition
2.0 ms pulse  -> anden yderposition
```
