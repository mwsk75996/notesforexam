# Kommunikationsprotokoller: I2C, SPI, UART

Når mikrokontrolleren snakker med sensorer og displays, bruges seriel kommunikation. Protokollerne adskiller sig på hastighed, antal ledninger og netværksstruktur.

### Transmissionsretninger (Duplex-tilstande)
1. **Simplex**: Én-vejs kommunikation. Data sendes kun fra sender til modtager (fx en simpel temperatursensor med en enkelt data-ledning, der kun sender).
2. **Half-duplex**: To-vejs kommunikation, men **kun én retning ad gangen**. Enhederne skal skiftes til at sende og modtage på samme linje (fx I2C).
3. **Full-duplex**: Simultan to-vejs kommunikation. Begge enheder kan sende og modtage samtidigt, typisk via to separate ledninger (fx UART og SPI).

### Sammenligningstabel for protokoller:

| Protokol | Type | Ledninger (ex. strøm) | Duplex | Hastighed | Enheder (Netværk) | Pull-up påkrævet? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UART** | Asynkron (intet clock-signal) | 2 (TX, RX) | Full-duplex | Langsom til medium (typisk 115200 bps) | Point-to-Point (kun 2 enheder) | Nej (normalt drevet aktivt) |
| **I2C** | Synkron (clock-styret) | 2 (SDA, SCL) | Half-duplex | Medium (100 kHz - 400 kHz) | Multi-master / Multi-slave (adresse-baseret) | **Ja** (SDA/SCL skal have pull-up modstande til VCC, typisk 4.7k$\Omega$) |
| **SPI** | Synkron | 3-4+ (MOSI, MISO, SCK, CS/SS) | Full-duplex | Meget hurtig (flere MHz) | 1 Master, flere slaves (kræver en CS-linje pr. slave) | Nej |

---
