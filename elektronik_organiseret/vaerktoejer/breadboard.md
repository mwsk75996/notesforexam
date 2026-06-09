# Værktøjer til Elektronik og Udvikling

### Breadboards (Hulprint)
- **Opbygning**: Bruges til hurtig prototype-bygning uden lodning.
  - **Yderbaner (Power rails)**: Kører lodret (eller vandret i toppen/bunden) langs hele brættet. Bruges til VCC ($3.3\text{V}/5\text{V}$) og GND.
  - **Inderbaner**: Forbundet i grupper af 5 huller på tværs (vinkelret på power rails).
  - **Midterdelingen**: Adskiller de to sider og passer præcist til bredden på IC'er og ESP32, så benene på hver side ikke kortsluttes.

### Lodning (Soldering)
- **Tips & Tricks**:
  - **Rengøring**: Hold loddekolbens spids ren med messinguld eller en fugtig svamp.
  - **Fortinning (Tinning)**: Kom altid en smule frisk tin på spidsen før lodning. Det forbedrer varmeoverførslen og beskytter spidsen mod oxidation.
  - **Teknik**: Varm både komponentbenet og kobberbanen på printkortet op samtidigt med kolben i 2-3 sekunder. Tilfør derefter tin til **samlingen** (ikke direkte på kolbespidsen), lad tinnet flyde ud, fjern tinnet, og fjern til sidst kolben. Hold samlingen helt stille, til tinnet er størknet.
  - **Kold lodning (Cold joint)**: Opstår hvis samlingen ikke blev varm nok, eller hvis komponenten flyttede sig under afkøling. Kendetegnes ved en mat, grålig, ru eller kugleformet overflade. Giver dårlig elektrisk forbindelse og knækker nemt mekanisk.

### Falstad
Falstad er en interaktiv, web-baseret kredsløbssimulator. Den er fremragende til at tegne kredsløb og visualisere strømmens retning (animerede prikker) og spændinger (farver) over tid. God til at teste spændingsdelere, filtre og 555-timere virtuelt, før man bygger dem i virkeligheden.

### KiCad Design-workflow
KiCad er det softwareprogram, I skal bruge til at designe kredsløb og PCB'er (printkort). Flowet består af:
1. **Schematic Editor (Eeschema - Diagramtegning)**:
   - Placer symboler for dine komponenter (fx ESP32, MQ-135, OLED).
   - Forbind komponenternes ben med ledninger (Wires) eller Net Labels.
   - Kør **ERC (Electrical Rules Check)** for at sikre, at der ikke er uforbundne pins, glemte strømforsyninger eller direkte kortslutninger.
2. **Footprint Association (Komponent-kobling)**:
   - Forbind hvert skematisk symbol med et fysisk footprint (layout-pakke, fx en $0.25\text{W}$ modstand eller et 38-pin DIP-modul).
3. **PCB Editor (Pcbnew - Boardlayout)**:
   - Definer printkortets fysiske form (Edge.Cuts-laget).
   - Placer komponenternes footprints hensigtsmæssigt.
   - Forbind komponenterne med kobberbaner (Tracks) på top- og bundlag (F.Cu / B.Cu).
   - Opret **Ground Planes (Copper Fills)** til GND for at reducere elektrisk støj.
   - Kør **DRC (Design Rules Check)** for at verificere, at banerne ikke ligger for tæt, er for tynde til strømmen, eller overtræder fabrikationsgrænserne.

### Funktionsgenerator
- **Hvad er det**: Et laboratorieapparat, der genererer elektriske spændingsbølger med kontrolleret frekvens, form og amplitude.
- **Waveforms (Bølgeformer)**:
  - **Sinusbølge**: Blød, harmonisk svingning. Bruges ofte til lyd- og radiotests.
  - **Firkantbølge**: Skifter øjeblikkeligt mellem to niveauer (HIGH/LOW). Bruges til clock-signaler og digitale kredsløb.
  - **Pulsbølge**: En firkantbølge, hvor bredden af pulsen (duty cycle) kan justeres uafhængigt.
  - **Trekantbølge**: Stiger og falder helt lineært. Bruges til analoge sweep-kredsløb.
  - **Savtandsbølge**: Stiger lineært og falder stejlt lodret (eller omvendt).
- **Parametre**:
  - `Frekvens`: Antal svingninger pr. sekund (Hz).
  - `Amplitude`: Spændingshøjden målt Peak-to-Peak ($V_{pp}$), fx fra $-5\text{V}$ til $+5\text{V}$ ($10V_{pp}$).
  - `DC Offset`: Lægger en konstant jævnspænding under signalet, så det fx flyttes op i det positive område ($0-3.3\text{V}$ i stedet for $-1.65\text{V}$ til $+1.65\text{V}$).
