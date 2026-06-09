# Dioder og Transistorer

### Dioder (Ensrettere)
Dioder tillader kun strøm at løbe i én retning (fra Anode [+] til Katode [-], markeret med en ring på komponenten).
- **Spændingsfald ($U_f$)**: Når dioden leder, falder der en spænding over den.
  - Almindelig Silicium-diode (fx 1N4007): $\approx 0.7\text{V}$
  - Schottky-diode (hurtigere, lavere tab): $\approx 0.3\text{V}$ (bruges ofte til ensretning og beskyttelse mod forkert polaritet).
  - LED (Lysdiode): Typisk $1.8\text{V}$ (rød) til $3.3\text{V}$ (blå/hvid). Kræver altid en seriemodstand for at begrænse strømmen.
  - Zener-diode: Designet til at lede "baglæns" (breakdown) ved en meget præcis spænding. Bruges til spændingsregulering og beskyttelse.

### Transistorer (BJT og MOSFET)
Transistorer fungerer som elektroniske kontakter eller forstærkere.

1. **BJT (Bipolar Junction Transistor)**:
   - **Styring**: Strømstyret. En lille strøm på Basen ($I_B$) styrer en stor strøm mellem Collector ($C$) og Emitter ($E$).
     $$I_C = \beta \cdot I_B$$
   - **Typer**: **NPN** (tænder ved HIGH spænding på base i forhold til emitter) og **PNP** (tænder ved LOW spænding).
   - **Ben**: Base (B), Collector (C), Emitter (E).

2. **MOSFET (Field-Effect Transistor)**:
   - **Styring**: Spændingsstyret. Spændingen mellem Gate og Source ($U_{GS}$) styrer modstanden ($R_{DS(on)}$) mellem Drain ($D$) og Source ($S$). Da Gate er isoleret, løber der stort set ingen strøm ind i Gate (høj indgangsimpedans).
   - **Typer**: **N-channel** (tænder når $U_{GS} > U_{threshold}$ - typisk HIGH logik) og **P-channel** (tænder når $U_{GS} < 0$ - typisk LOW logik).
   - **Ben**: Gate (G), Drain (D), Source (S).
   - *MOSFET er ideel som switch til høje strømme (fx motorstyring), fordi dens tændte modstand ($R_{DS(on)}$) er ekstremt lav, hvilket minimerer varmeafgivelse.*

---
