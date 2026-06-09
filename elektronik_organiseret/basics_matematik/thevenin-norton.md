# Thevenin og Norton

Thevenin og Norton bruges til at forenkle komplekse, lineære kredsløb med flere modstande og kilder til et simpelt ækvivalent kredsløb set fra en loads (fx en sensors) synspunkt.

### Thevenin-ækvivalent (Spændingsform)
Forenkler kredsløbet til én spændingskilde ($V_{th}$) i serie med én modstand ($R_{th}$).
```text
  Stort kredsløb  -->  Vth --- [Rth] --- A
                                         |  <-- Load (RL) tilkobles her
                                         B (GND)
```
**Fremgangsmåde**:
1. **Fjern load-modstanden** ($R_L$) så terminalerne A og B er åbne.
2. **Find $V_{th}$**: Beregn spændingen mellem A og B. Dette kaldes åben-kreds-spændingen ($V_{oc}$).
3. **Find $R_{th}$**: Sluk alle uafhængige kilder i kredsløbet og find modstanden set mellem A og B:
   - En ideel spændingskilde erstattes med en **kortslutning** (en ledning).
   - En ideel strømkilde erstattes med en **åben forbindelse** (fjernes).
4. **Tegn kredsløbet** med $V_{th}$ i serie med $R_{th}$ og $R_L$.

---

### Norton-ækvivalent (Strømform)
Forenkler kredsløbet til én strømkilde ($I_N$) i parallel med én modstand ($R_N$).
```text
                       +-------- A
                       |        |
  Stort kredsløb  --> (IN)     [RN]  <-- Load (RL) tilkobles her
                       |        |
                       +-------- B
```
**Fremgangsmåde**:
1. Kortslut terminalerne A og B.
2. **Find $I_N$**: Beregn strømmen, der løber gennem denne kortslutning. Dette kaldes kortslutningsstrømmen ($I_{sc}$).
3. **Find $R_N$**: Find modstanden set mellem A og B på samme måde som for $R_{th}$. Der gælder altid:
   $$R_N = R_{th}$$

### Sammenhæng mellem Thevenin og Norton (Kilde-transformation)
Du kan frit transformere mellem de to ækvivalenter vha. Ohms lov:
- **Fra Thevenin til Norton**:
  $$I_N = \frac{V_{th}}{R_{th}}$$
- **Fra Norton til Thevenin**:
  $$V_{th} = I_N \cdot R_N$$
- **Modstanden** er den samme:
  $$R_{th} = R_N$$


## Thevenin eksempel

Forestil dig dette kredsløb:

```text
12V -- R1 1k -- punkt A -- R2 2k -- GND
                  |
                  +-- RL 3k -- GND
```

`RL` er load-modstanden. Det kan fx være en sensor, en LED-del eller et andet kredsløb der er koblet på punkt A.

Målet er at forenkle alt til venstre for `RL`, så loaden kun ser:

```text
Vth -- Rth -- RL -- GND
```

### 1. Fjern loaden

Først fjerner vi `RL`, så punkt A er åben.

```text
12V -- R1 1k -- punkt A -- R2 2k -- GND
```

Nu er kredsløbet bare en spændingsdeler.

### 2. Find Vth

`Vth` er spændingen på punkt A uden load.

```text
Vth = Vin * R2 / (R1 + R2)
Vth = 12V * 2k / (1k + 2k)
Vth = 12V * 2 / 3
Vth = 8V
```

Så Thevenin-spændingen er:

```text
Vth = 8V
```

### 3. Find Rth

Nu skal vi finde modstanden set ind i punkt A.

Vi slukker spændingskilden. En ideel spændingskilde bliver til en kortslutning.

Det betyder at `12V` bliver til `GND`.

```text
GND -- R1 1k -- punkt A -- R2 2k -- GND
```

Set fra punkt A går både `R1` og `R2` til GND. De ligger derfor parallelt.

```text
Rth = R1 || R2
Rth = (R1 * R2) / (R1 + R2)
Rth = (1k * 2k) / (1k + 2k)
Rth = 2000k / 3k
Rth = 0.667k
Rth = 667 Ohm
```

Så Thevenin-modstanden er:

```text
Rth = 667 Ohm
```

### 4. Tegn det forenklede kredsløb

Nu kan hele kredsløbet til venstre for `RL` erstattes med:

```text
8V -- Rth 667 Ohm -- RL 3k -- GND
```

Det er meget nemmere at regne på.

### 5. Beregn spændingen over loaden

Nu er `Rth` og `RL` bare en ny spændingsdeler.

```text
V_RL = Vth * RL / (Rth + RL)
V_RL = 8V * 3000 / (667 + 3000)
V_RL = 8V * 3000 / 3667
V_RL = 6.54V
```

Så når loaden sættes på, falder spændingen fra `8V` til cirka `6.54V`.

Det er pointen med Thevenin: uden load ser punkt A ud som `8V`, men når loaden trækker strøm, falder spændingen på grund af den interne Thevenin-modstand.

Kort eksamenssvar:

> Først fjerner jeg loaden og finder åben-kreds-spændingen som `Vth`. Derefter slukker jeg spændingskilden og finder modstanden set fra loadens terminaler som `Rth`. Til sidst erstatter jeg hele kredsløbet med en spændingskilde og en seriemodstand, så det er nemmere at beregne load-spænding og load-strøm.

God eksamensforklaring:

> Thevenin gør det nemmere at regne på en load. I stedet for at regne på hele kredsløbet hver gang, laver man en ækvivalent spændingskilde med en intern modstand.
