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

### AND

Output er kun `1` hvis begge inputs er `1`.

```text
A B | X
0 0 | 0
0 1 | 0
1 0 | 0
1 1 | 1
```

### OR

Output er `1` hvis mindst ét input er `1`.

```text
A B | X
0 0 | 0
0 1 | 1
1 0 | 1
1 1 | 1
```

### NOT

Output er det modsatte af input.

```text
A | X
0 | 1
1 | 0
```

### XOR

Output er `1` hvis inputs er forskellige.

```text
A B | X
0 0 | 0
0 1 | 1
1 0 | 1
1 1 | 0
```

### NAND

NOT AND.

```text
A B | X
0 0 | 1
0 1 | 1
1 0 | 1
1 1 | 0
```

### NOR

NOT OR.

```text
A B | X
0 0 | 1
0 1 | 0
1 0 | 0
1 1 | 0
```

## Eksempler med tre inputs

Hvis en sandhedstabel kun er `1` når alle inputs er `1`, er det:

```text
X = A AND B AND C
```

Hvis en sandhedstabel er `1` når A, B eller C er `1`, men `0` ved flere inputs samtidig, kan det ligne XOR-logik.

God metode:

1. Find alle rækker hvor `X = 1`.
2. Skriv hvilke inputs der er `1` eller `0`.
3. Se om det matcher AND, OR, XOR, NAND eller kombinationer.

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
