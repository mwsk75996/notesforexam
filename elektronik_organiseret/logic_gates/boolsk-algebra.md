# Boolsk Algebra: Love og Axiomer

Boolsk algebra bruges til at reducere og simplificere logiske udtryk, så de kan bygges med færre fysiske logic gates.

### Grundlæggende aksiomer (Regneregler):
- **Identitet**: $A \cdot 1 = A$ og $A + 0 = A$
- **Nul-element**: $A \cdot 0 = 0$ og $A + 1 = 1$
- **Idempotens**: $A \cdot A = A$ og $A + A = A$
- **Komplement**: $A \cdot A' = 0$ og $A + A' = 1$
- **Dobbelt negation**: $(A')' = A$

### Matematiske teoremer:
- **Kommutative lov**: $A \cdot B = B \cdot A$ og $A + B = B + A$
- **Associative lov**: $(A \cdot B) \cdot C = A \cdot (B \cdot C)$ og $(A + B) + C = A + (B + C)$
- **Distributive lov**:
  - $A \cdot (B + C) = (A \cdot B) + (A \cdot C)$
  - $A + (B \cdot C) = (A + B) \cdot (A + C)$ *(Bemærk: Denne gælder kun i boolsk algebra!)*
- **Absorptionsloven** (meget nyttig til simplificering):
  - $A + (A \cdot B) = A$
  - $A \cdot (A + B) = A$

### De Morgans Love (Ekstremt vigtige!)
De Morgans love gør det muligt at bryde en negation (NOT-streg) over et helt udtryk:
1. **Første lov (Negation af en sum)**:
   $$(A + B)' = A' \cdot B' \quad \text{eller} \quad \neg(A \vee B) = \neg A \wedge \neg B$$
   *(NOT OR svarer til at invertere hvert led og lave det til AND).*
2. **Anden lov (Negation af et produkt)**:
   $$(A \cdot B)' = A' + B' \quad \text{eller} \quad \neg(A \wedge B) = \neg A \vee \neg B$$
   *(NOT AND svarer til at invertere hvert led og lave det til OR).*

**Vigtig eksamensanvendelse**:
> Hvis vi fx skal bygge et NOR-kredsløb, men kun har NAND-gates til rådighed, kan vi bruge De Morgans love til at omskrive det logiske udtryk, så det passer til de komponenter, vi har i skuffen.

---
