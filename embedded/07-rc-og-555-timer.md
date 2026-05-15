# RC-kredsløb og 555 timer

## RC-kredsløb

Et RC-kredsløb består af:

- `R` modstand
- `C` kondensator

Tidskonstanten hedder tau:

```text
tau = R * C
```

Hvor:

- `R` er ohm
- `C` er farad
- `tau` er sekunder

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
