# LiPo batteri

Et 1S LiPo batteri har typisk:

```text
Nominel spænding: 3.7V
Fuldt opladet:    4.2V
Næsten tomt:      3.0V
```

Man skal ikke aflade et LiPo for langt ned, da det kan skade batteriet.


## Oplader modul

Typisk LiPo charger-modul:

- `5V` input
- `BAT+` og `BAT-` til batteriet
- Rød LED betyder oplader
- Blå LED betyder fuldt opladet
- Stopper automatisk når batteriet er fuldt


## Driftstid

Simpel formel:

```text
driftstid i timer = kapacitet i mAh / strømforbrug i mA
```

Eksempel:

```text
Batteri = 2000 mAh
Forbrug = 500 mA

driftstid = 2000 / 500 = 4 timer
```

I praksis bliver det ofte lidt mindre på grund af tab i regulatorer og varierende strømforbrug.

Vigtigt:

> mAh alene fortæller ikke hele historien. Et batteri med høj kapacitet kan stadig være dårligt valg, hvis det ikke kan levere nok strøm til motorer, servoer og ESP32 samtidig.


## Praktisk rover-strøm og batteriopbygning

Fra jeres batteri/display-opgave:
- Brug fælles GND.
- Brug sikring på batteriet, fx `3-5A`.
- Brug main switch.
- Brug kondensatorer på output, fx `1000 uF`.
- Servoer/motorer bør ikke drives direkte fra ESP32.
- ESP32 skal have stabil `3.3V` eller passende `VIN/5V`, afhængigt af board.

### Batterikombinationer
- **Serieforbindelse (Series)**: Spændingen lægges sammen, kapaciteten er uændret.
  $$U_{total} = U_1 + U_2 + \dots, \quad Capacity_{total} = Capacity_{1}$$
  *Eksempel*: To $3.7\text{V}$ $2000\text{mAh}$ celler i serie (2S) giver $7.4\text{V}$ og $2000\text{mAh}$.
- **Parallelforbindelse (Parallel)**: Kapaciteten lægges sammen, spændingen er uændret.
  $$Capacity_{total} = Capacity_1 + Capacity_2 + \dots, \quad U_{total} = U_1$$
  *Eksempel*: To $3.7\text{V}$ $2000\text{mAh}$ celler i parallel (1S2P) giver $3.7\text{V}$ og $4000\text{mAh}$.
  *VIGTIGT*: Batterierne skal have nøjagtig samme spænding (indenfor $\pm0.05\text{V}$) inden de kobles sammen for at undgå enorme udligningsstrømme og brandfare.

---
