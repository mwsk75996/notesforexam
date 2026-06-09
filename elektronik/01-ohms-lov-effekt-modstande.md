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

Modstande aflæses med farveringe. Typisk har de 4 eller 5 ringe:
- **4-rings modstand**: 1. ring (1. ciffer), 2. ring (2. ciffer), 3. ring (multiplikator $10^x$), 4. ring (tolerance).
- **5-rings modstand**: 1. ring (1. ciffer), 2. ring (2. ciffer), 3. ring (3. ciffer), 4. ring (multiplikator $10^x$), 5. ring (tolerance).

### Farvetabel:
- **Cifre**: Sort (0), Brun (1), Rød (2), Orange (3), Gul (4), Grøn (5), Blå (6), Violet (7), Grå (8), Hvid (9)
- **Multiplikator**: Sort ($1$), Brun ($10$), Rød ($100$), Orange ($1\text{k}$), Gul ($10\text{k}$), Grøn ($100\text{k}$), Blå ($1\text{M}$), Guld ($0.1$), Sølv ($0.01$)
- **Tolerance**: Guld ($\pm 5\%$), Sølv ($\pm 10\%$), Brun ($\pm 1\%$), Rød ($\pm 2\%$)

Eksempler fra opgaverne:
- **4-rings**: `Rød (2) - Violet (7) - Orange (1k) - Brun (1%)` = $27\text{ kOhm} \pm 1\%$
- **4-rings**: `Brun (1) - Grøn (5) - Gul (10k) - Guld (5%)` = $150\text{ kOhm} \pm 5\%$
- **5-rings**: `Orange (3) - Brun (1) - Blå (6) - Brun (10) - Brun (1%)` = $316 \times 10 = 3160\text{ Ohm} \pm 1\%$

---

## Seriel, parallel og kombineret kredsløb

### Serieforbindelse (Seriel)
- Modstandene ligger i forlængelse af hinanden.
- Strømmen ($I$) er den samme igennem alle modstande: $I_{total} = I_1 = I_2 = \dots$
- Spændingen ($U$) deles over modstandene: $U_{total} = U_1 + U_2 + \dots$
- Den samlede modstand ($R_{eq}$):
  $$R_{eq} = R_1 + R_2 + R_3 + \dots$$

### Parallelforbindelse
- Modstandene er forbundet over de samme to knudepunkter.
- Spændingen ($U$) er den samme over alle modstande: $U_{total} = U_1 = U_2 = \dots$
- Strømmen ($I$) deles ud i grenene: $I_{total} = I_1 + I_2 + \dots$
- Den samlede modstand ($R_{eq}$):
  $$\frac{1}{R_{eq}} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3} + \dots$$
  For to modstande kan man bruge genvejen:
  $$R_{eq} = \frac{R_1 \cdot R_2}{R_1 + R_2}$$

### Kombineret kredsløb
- Kredsløb, som indeholder både serielle og parallelle forbindelser.
- **Fremgangsmåde**:
  1. Identificer parallelle modstandsgrupper og erstat dem med en enkelt ækvivalent modstand ($R_{parallel}$).
  2. Læg denne værdi sammen med de modstande, der ligger i serie med gruppen.

---

## Kirchhoffs Love

### 1. Kirchhoffs Strømlov (KCL - Current Law)
- Strømmen ind i et knudepunkt er lig med strømmen ud af knudepunktet. Elektrisk ladning kan ikke ophobe sig eller forsvinde.
- Formel:
  $$\sum I_{ind} = \sum I_{ud}$$

### 2. Kirchhoffs Spændingslov (KVL - Voltage Law)
- Summen af alle elektriske potentialeforskelle (spændinger) rundt i en lukket sløjfe (loop) er altid 0.
- Formel:
  $$\sum U_{sløjfe} = 0$$
  *(Dvs. spændingen leveret af en strømkilde er lig med summen af spændingsfaldene over modstandene i sløjfen).*

---

## Multimeter og målinger

Brug multimeteret til at kontrollere dit kredsløb:
- **Måle spænding (V)**: Måles **parallelt** over den komponent, du vil kende spændingsfaldet over. Kredsløbet skal være tændt.
- **Måle strøm (A)**: Måles **i serie**. Du skal afbryde kredsløbet og lade strømmen løbe igennem multimeteret.
- **Måle modstand ($\Omega$)**: Måles over komponenten **uden strøm** på kredsløbet (afbryd strømkilden helt, ellers ødelægges målingen eller multimeteret).
- **Kontinuitetstest (Bip)**: Bruges til at tjekke for uønskede kortslutninger eller bekræfte, at der er elektrisk forbindelse (fx at GND er fælles i hele kredsløbet).

**Vigtig eksamensforklaring**:
> Ohms lov bruges til at finde den manglende værdi i kredsløbet. Hvis jeg kender spænding og strøm, kan jeg finde modstanden. Effektformlen bruges bagefter til at se, hvor meget energi komponenten afsætter som varme, så vi sikrer, at modstandens watt-rating (fx 0.25W) ikke overskrides.
