# Modstand farvekoder

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
