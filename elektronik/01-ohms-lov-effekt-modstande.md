# Ohms lov, effekt og modstande

Ohms lov bruges til at regne sammenhængen mellem spænding, strøm og modstand.

```text
U = R * I
I = U / R
R = U / I
```

Hvor:

- `U` er spænding i volt `V`
- `I` er strøm i ampere `A`
- `R` er modstand i ohm `Ohm`

Husk:

```text
1 A = 1000 mA
50 mA = 0.05 A
```

Eksempel:

Hvis en LED/kreds bruger `50 mA` ved `5V`:

```text
R = U / I
R = 5V / 0.05A
R = 100 Ohm
```

## Effekt

Effekt er hvor meget energi kredsløbet bruger per sekund.

```text
P = U * I
U = P / I
I = P / U
```

Hvor:

- `P` er effekt i watt `W`
- `U` er spænding i volt `V`
- `I` er strøm i ampere `A`

Eksempel:

```text
U = 5V
I = 0.2A

P = 5V * 0.2A = 1W
```

Hvis en komponent bruger meget effekt, bliver den typisk varm. Derfor skal man tænke over både spænding, strøm og watt-rating på komponenter.

## Modstand farvekoder

Modstande kan aflæses med farver.

Eksempler fra opgaverne:

```text
Rød - Violet - Gul - Brun = 27 kOhm +-1%
Brun - Grøn - Grøn - Guld = 150 kOhm +-5%
Orange - Brun - Blå - Brun - Brun = 3160 Ohm +-1%
```

God eksamensforklaring:

> Ohms lov bruges til at finde den manglende værdi i kredsløbet. Hvis jeg kender spænding og strøm, kan jeg finde modstanden. Effektformlen bruges bagefter til at se hvor meget energi komponenten bruger, og om komponenten kan holde til belastningen.

## Multimeter

Brug multimeter til:

- Måle spænding over en komponent
- Måle modstand når kredsløbet er slukket
- Måle kontinuitet for at se om der er forbindelse
- Tjekke om GND faktisk er fælles

Vigtigt:

- Spænding måles parallelt.
- Strøm måles i serie.
- Modstand måles uden strøm på kredsløbet.
