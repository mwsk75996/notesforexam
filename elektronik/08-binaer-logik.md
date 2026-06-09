# Binær og logik

## Binær til decimal

Binær er base 2. Hver plads er en potens af 2.

```text
128 64 32 16 8 4 2 1
```

Eksempel:

```text
10000010
= 128 + 2
= 130
```

Eksempel:

```text
1100100
= 64 + 32 + 4
= 100
```

## Decimal til binær

Find hvilke 2-potenser der kan lægges sammen.

Eksempel:

```text
35 = 32 + 2 + 1
35 = 100011
```

Eksempel:

```text
170 = 128 + 32 + 8 + 2
170 = 10101010
```

Eksempel:

```text
200 = 128 + 64 + 8
200 = 11001000
```

## Logiske gates

I digital logik bruger man ofte matematiske tegn til at skrive gates kortere.

Vigtigt: `+` og `.` betyder her boolsk logik, ikke normal plus og gange.

```text
Gate      Tegn              Eksempel
AND       ∧ eller .          X = A ∧ B      eller X = A . B
OR        ∨ eller +          X = A ∨ B      eller X = A + B
NOT       ¬ eller streg      X = ¬A         eller X = A'
XOR       ⊕                  X = A ⊕ B
NAND      ¬(A ∧ B)           X = ¬(A ∧ B)
NOR       ¬(A ∨ B)           X = ¬(A ∨ B)
AND-NOT   A ∧ ¬B             X = A ∧ ¬B
```

### AND

Output er kun `1` hvis begge inputs er `1`.

Matematisk:

```text
X = A ∧ B
X = A . B
```

```text
A B | X
0 0 | 0
0 1 | 0
1 0 | 0
1 1 | 1
```

### OR

Output er `1` hvis mindst ét input er `1`.

Matematisk:

```text
X = A ∨ B
X = A + B
```

```text
A B | X
0 0 | 0
0 1 | 1
1 0 | 1
1 1 | 1
```

### NOT

Output er det modsatte af input.

Matematisk:

```text
X = ¬A
X = A'
```

```text
A | X
0 | 1
1 | 0
```

### XOR

Output er `1` hvis inputs er forskellige.

Matematisk:

```text
X = A ⊕ B
```

```text
A B | X
0 0 | 0
0 1 | 1
1 0 | 1
1 1 | 0
```

### NAND

NOT AND.

Matematisk:

```text
X = ¬(A ∧ B)
X = (A . B)'
```

```text
A B | X
0 0 | 1
0 1 | 1
1 0 | 1
1 1 | 0
```

### NOR

NOT OR.

Matematisk:

```text
X = ¬(A ∨ B)
X = (A + B)'
```

```text
A B | X
0 0 | 1
0 1 | 0
1 0 | 0
1 1 | 0
```

### AND-NOT

AND-NOT betyder `A AND NOT B`.

Matematisk:
```text
X = A ∧ ¬B
X = A . B'
```

```text
A B | X
0 0 | 0
0 1 | 0
1 0 | 1
1 1 | 0
```

---

## Boolsk Algebra: Love og Axiomer

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

## Eksempler med tre inputs

Hvis en sandhedstabel kun er `1` når alle inputs er `1`, er det:

```text
X = A AND B AND C
X = A ∧ B ∧ C
```

Hvis en sandhedstabel er `1` når A, B eller C er `1`, men `0` ved flere inputs samtidig, kan det ligne XOR-logik.

God metode:

1. Find alle rækker hvor `X = 1`.
2. Skriv hvilke inputs der er `1` eller `0`.
3. Se om det matcher AND, OR, XOR, NAND, NOR, AND-NOT eller kombinationer.

Eksempel:

```text
A B C | X
0 0 0 | 0
1 0 0 | 1
0 1 0 | 1
0 0 1 | 1
1 1 0 | 0
1 0 1 | 0
0 1 1 | 0
1 1 1 | 0
```

Her er output `1` når præcis ét input er `1`.

God eksamensforklaring:

> En sandhedstabel viser alle mulige inputkombinationer og hvad output bliver. Når man skal finde logikken, starter man med de rækker hvor output er 1.
