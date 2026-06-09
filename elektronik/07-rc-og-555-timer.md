# RC-kredsløb og 555 timer

## RC-kredsløb og Kondensator-typer

Et RC-kredsløb består af en modstand ($R$) og en kondensator ($C$).

### Kondensatorer (Capacitors)
En kondensator lagrer elektrisk energi i et elektrisk felt mellem to ledende plader adskilt af et isolerende materiale (dielektrikum).
- **Polariserede kondensatorer**: Skal vendes rigtigt i kredsløbet. Den positive terminal (Anode, længere ben) skal til højere spænding end den negative (Katode, markeret med en stribe eller minustegn på huset).
  - *Elektrolytkondensator (Elektrolyt)*: Har typisk store kapaciteter (fra $1\mu\text{F}$ til flere tusinde $\mu\text{F}$). Bruges som energibuffer og spændingsstabilisator. Kan eksplodere eller kortslutte, hvis de vendes forkert!
  - *Tantalkondensator*: Kompakte, meget stabile, men følsomme over for spændingsspidser.
- **Ikke-polariserede kondensatorer**: Kan vendes vilkårligt.
  - *Keramisk kondensator*: Hurtige, har typisk små kapaciteter (fra $1\text{ pF}$ til $1\mu\text{F}$). Bruges tæt på IC'er/sensorer til at fjerne højfrekvent støj (afkobling/decoupling, typisk $100\text{ nF}$).
  - *Foliekondensator*: Bruges ofte i analoge filtre pga. høj præcision.

### Kondensatorkombinationer (Modsat af modstande!)
- **Parallelforbindelse**: Kapacitansen lægges sammen (pladearealet forøges):
  $$C_{eq} = C_1 + C_2 + C_3 + \dots$$
- **Serieforbindelse**: Den reciproke værdi lægges sammen:
  $$\frac{1}{C_{eq}} = \frac{1}{C_1} + \frac{1}{C_2} + \frac{1}{C_3} + \dots$$
  For to kondensatorer:
  $$C_{eq} = \frac{C_1 \cdot C_2}{C_1 + C_2}$$

---

### Tidskonstanten Tau ($\tau$)
Tidskonstanten angiver hastigheden for opladning/afladning:
$$\tau = R \cdot C$$

Hvor:
- $R$ er modstanden i Ohm ($\Omega$)
- $C$ er kapacitansen i Farad ($\text{F}$)
- $\tau$ er tidskonstanten i sekunder ($\text{s}$)

## Opladning og afladning

Ved opladning:

```text
1 tau = cirka 63%
3 tau = cirka 95%
5 tau = cirka 99%
```

Ved afladning:

```text
1 tau = cirka 37% tilbage
```

God forklaring:

> Kondensatoren oplades ikke lineært. Den stiger hurtigt i starten og langsommere når den nærmer sig forsyningsspændingen.

## 555 timer

555 timer kan bruges i tre typiske modes:

- Astable
- Monostable
- Bistable

## Astable

Astable betyder at output skifter af sig selv.

Bruges til:

- Blinkende LED
- Clock signal
- Simpel oscillator

Forklaring:

> I astable mode har 555 timeren ingen stabil tilstand. Den skifter hele tiden mellem HIGH og LOW.

På oscilloskop kan man se en firkantbølge. Den er ikke altid perfekt symmetrisk, fordi opladning og afladning går gennem forskellige modstande.

## Monostable

Monostable betyder én stabil tilstand.

Bruges til:

- Knap starter en puls
- Timer
- Toaster-lignende funktion

Forklaring:

> I monostable mode er output normalt LOW. Når triggeren aktiveres, går output HIGH i en bestemt tid og falder derefter tilbage.

Eksempel fra opgaven:

```text
Knap trykkes -> LED tænder i en periode -> LED slukker igen
```

## Bistable

Bistable betyder to stabile tilstande.

Bruges til:

- Toggle on/off
- Simpel hukommelse
- Latch

Forklaring:

> I bistable mode kan 555 timeren huske om output er HIGH eller LOW, indtil den bliver sat eller reset.

## Toaster-eksempel

Fra RC/555-opgaven:

- Knap starter timeren.
- Potentiometer sætter tiden.
- RC-kredsløb bestemmer tidsforsinkelse.
- 555 timer kører i monostable mode.

God eksamensforklaring:

> RC-leddet bestemmer hvor hurtigt kondensatoren oplades. Når spændingen rammer trigger/threshold-niveauet i 555 timeren, skifter output. Derfor kan R og C bruges til at styre tiden.
