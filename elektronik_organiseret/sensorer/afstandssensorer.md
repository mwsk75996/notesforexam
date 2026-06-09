# Ultralyd vs. Time-of-Flight (ToF)

Begge sensorer bruges til afstandsmåling:

### Ultralyd (fx HC-SR04)
- **Princip**: Sender en ultralydslydbølge (Trigger) afsted og måler tiden ($t$), indtil ekkoet (Echo) vender tilbage.
- **Formel**:
  $$d = \frac{v_{lyd} \cdot t}{2}$$
  Hvor $v_{lyd} \approx 343\text{ m/s}$ ($0.0343\text{ cm/}\mu\text{s}$ ved $20^\circ\text{C}$). Division med 2 skyldes, at lyden skal rejse frem og tilbage.
- **Ulempe**: Lydbølger spreder sig kegleformet. Bløde overflader absorberer lyden, og skrå vægge kan kaste ekkoet væk, så målingen fejler.

### Time-of-Flight (ToF, fx VL53L0X)
- **Princip**: Sender en mikroskopisk, usynlig infrarød laserpuls afsted og måler tiden, det tager for lyset at blive reflekteret tilbage til sensoren.
- **Fordel**: Ekstremt præcis og måler i en snæver stråle (ikke en bred kegle). Påvirkes ikke af overfladens vinkel eller materiale i samme grad som ultralyd.
- **Ulempe**: Kan forstyrres af stærkt sollys (infrarød støj) og har kortere rækkevidde (typisk 1-2 meter).

---
