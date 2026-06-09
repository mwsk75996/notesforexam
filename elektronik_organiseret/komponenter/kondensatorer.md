# RC-kredsløb og Kondensator-typer

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
