# Boost og buck converter

En boost converter hæver spændingen.

```text
3.7V batteri -> 5V output
```

En buck converter sænker spændingen.

```text
12V input -> 5V output
```

Effektivitet er typisk ikke 100%. Hvis en converter er 85-90% effektiv, skal batteriet levere mere effekt end outputtet bruger.

```text
P = U * I
```

Hvis output er:

```text
5V * 1A = 5W
```

Så skal batterisiden levere lidt mere end `5W`, fordi der er tab i converteren.

Eksempel med effektivitet:

```text
Output: 5V * 1A = 5W
Effektivitet: 85%

Input-effekt = 5W / 0.85 = 5.88W
```

Hvis batteriet er cirka `3.7V`:

```text
Input-strøm = 5.88W / 3.7V = 1.59A
```

Det betyder at en 5V converter der leverer `1A` ud, kan trække omkring `1.6A` fra et 1S LiPo batteri.
