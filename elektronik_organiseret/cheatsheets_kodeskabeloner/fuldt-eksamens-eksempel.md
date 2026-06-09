# Eksamens-guide: Indlejrede Systemer (ESP32, OLED & Gassensor)

Dette dokument er et komplet, samlet kodescenarie fokuseret **udelukkende på Indlejrede Systemer**, baseret på kravene i eksamensforberedelsen.

Det dækker opsætningen af **ESP32 Wroom 38-Pin**, **MQ135-MQ2 gassensoren** og **OLED 1.3” I2C** displayet (SH1106 driver) i PlatformIO.

---

## 1. platformio.ini Konfiguration

Opret et PlatformIO projekt og indsæt følgende i din `platformio.ini` for at hente de korrekte biblioteker til displayet:

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino

; Indstil Serial Monitor hastighed
monitor_speed = 115200

; Biblioteker til 1.3" SH1106 OLED
lib_deps =
    olikraus/U8g2 @ ^2.35.19
```

---

## 2. Firmware til ESP32 (`src/main.cpp`)

Dette program kører lokalt på ESP32. Det læser den analoge værdi fra gassensoren, evaluerer luftkvaliteten mod thresholds og udskriver resultaterne løbende på 1.3" OLED-displayet ved hjælp af SH1106-driveren i U8g2.

### Forbindelsesdiagram (Pinout):
- **OLED 1.3" (I2C)**:
  - `VCC` -> 3.3V
  - `GND` -> GND (Fælles stel)
  - `SDA` -> GPIO 21
  - `SCL` -> GPIO 22
- **MQ135 / MQ2 (Gas)**:
  - `VCC` -> **5V** *(Vigtigt: 5V er påkrævet til sensorens varmelegeme/heater)*
  - `GND` -> GND
  - `AOUT` -> GPIO 33 (ADC1)

### Kildekode:
```cpp
#include <Arduino.h>
#include <U8g2lib.h>
#include <Wire.h>

#define GAS_PIN 33 // AOUT fra gassensoren tilsluttet analog pin GPIO33 (ADC1)

// Konstruktør til 1.3" I2C OLED (SH1106 controller)
// U8G2_R0 = ingen rotation, F = fuld framebuffer, HW_I2C = hardware I2C
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void setup() {
    Serial.begin(115200);
    
    // Start I2C bussen med SDA=21 og SCL=22
    Wire.begin(21, 22);
    
    // Start displayet
    u8g2.begin();
    
    // Opstartsskærm / Status
    u8g2.clearBuffer();
    u8g2.setFont(u8g2_font_ncenB08_tr); // Vælg skrifttype
    u8g2.drawStr(0, 15, "ESP32 Wroom Klar");
    u8g2.drawStr(0, 35, "Varmer sensor op...");
    u8g2.sendBuffer();

    Serial.println("System opstartet. Varmer gassensor op...");
    delay(5000); // 5 sekunders opstartstest (anbefales 30 sek+ i virkeligheden)
}

void loop() {
    // 1. Læs den rå analoge værdi fra gassensoren (0 - 4095)
    int gasRaw = analogRead(GAS_PIN);
    float voltage = gasRaw * 3.3 / 4095.0; // Omregn til spænding

    // 2. Evaluer luftkvaliteten
    String statusStr = "";
    if (gasRaw < 200) {
        statusStr = "Status: Fremragende";
    } else if (gasRaw >= 200 && gasRaw <= 350) {
        statusStr = "Status: Moderat gas";
    } else {
        statusStr = "Status: DAARLIG LUFT!";
    }

    // Output til Serial Monitor (til debugging)
    Serial.print("Rå ADC: ");
    Serial.print(gasRaw);
    Serial.print("  |  Spænding: ");
    Serial.print(voltage);
    Serial.print(" V  |  ");
    Serial.println(statusStr);

    // 3. Opdater OLED displayet
    u8g2.clearBuffer();          // Ryd framebufferen
    u8g2.setFont(u8g2_font_ncenB08_tr);
    
    // Overskrift
    u8g2.drawStr(0, 15, "--- LUFTKVALITET ---");
    
    // Måleværdier
    char gasValStr[32];
    sprintf(gasValStr, "Raa ADC: %d", gasRaw);
    u8g2.drawStr(0, 35, gasValStr);
    
    char voltValStr[32];
    sprintf(voltValStr, "Spaending: %.2f V", voltage);
    u8g2.drawStr(0, 50, voltValStr);
    
    // Status
    u8g2.drawStr(0, 64, statusStr.c_str());
    
    u8g2.sendBuffer();           // Tegn skærmbilledet

    delay(1000); // Tag måling hvert sekund
}
```

---

## 3. KiCad Symbolforberedelse til Eksamen

Eksamensforberedelsen kræver, at du har downloadet eller oprettet KiCad symboler for de tre specifikke komponenter. Her er de vigtigste pin-specifikationer til dine symboler:

1. **ESP32 Wroom 38-Pin**:
   - Skal have 38 pins i alt.
   - Sørg for at markere `3.3V`, `5V/VIN`, og `GND` tydeligt som strømpins (Power Inputs).
   - Marker standard I2C pins `GPIO21 (SDA)` og `GPIO22 (SCL)`.
   - Marker ADC-pins til analoge sensorer (fx `GPIO33` til gassensor).

2. **MQ135-MQ2 Gassensor**:
   - Typisk 4 pins på breakout: `VCC` (5V), `GND`, `AOUT` (Analog Out), `DOUT` (Digital Out).
   - Dit skematiske symbol skal have disse 4 pins præcist defineret.

3. **Display OLED 1.3” I2C**:
   - 4 pins: `VCC` (3.3V), `GND`, `SDA`, `SCL`.

---

## 4. Fejlfindingstips til Eksamen
- **Ustabil I2C-forbindelse / "sne" på skærmen**: Tjek om du har byttet om på SDA (GPIO21) og SCL (GPIO22). Dobbelttjek at du anvender `U8G2_SH1106_128X64_NONAME_F_HW_I2C` konstruktøren i koden i stedet for en standard SSD1306 driver.
- **Fælles GND**: Husk at forbinde alle GND-ben (ESP32 GND, OLED GND og gassensorens GND) sammen på dit breadboard. Uden fælles GND vil målingerne svinge vildt eller fejle helt.
- **Gassensor-spænding**: Gassensoren skal have 5V ind på VCC. Hvis du ved en fejl slutter den til 3.3V, vil varmelegemet ikke fungere, og målingerne bliver statiske eller ubrugelige.
