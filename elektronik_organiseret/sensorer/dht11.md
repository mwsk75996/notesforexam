# DHT11 - Temperatur og Fugtighed

## Beskrivelse
DHT11 er en simpel digital sensor, der måler omgivende temperatur og relativ luftfugtighed. Data sendes digitalt over en enkelt ledning ved hjælp af en speciel seriel protokol. Den er langsom og har begrænset præcision, men er meget populær til simple indeklima-overvågninger og komfort-score beregninger.

### Egenskaber:
- **Signal**: Digital data-protokol (kræver software-afkodning via bibliotek).
- **Opdateringshastighed**: Bør højst læses hvert 1-2 sekund.
- **Præcision**: Temperatur: $\pm 2^\circ\text{C}$, Fugtighed: $\pm 5\%$.

### Typisk ledningsforbindelse (Wiring):
- **VCC**: 3.3V eller 5V
- **GND**: GND (Fælles stel)
- **DATA**: GPIO pin (fx GPIO 4). Data-linjen kræver typisk en $10\text{ k}\Omega$ pull-up modstand til VCC (ofte monteret på breakoutboardet).

---

## Kodeeksempel (PlatformIO / Arduino C++)
Kræver Adafruit `DHT sensor library` i `platformio.ini`:
```ini
lib_deps =
    adafruit/DHT sensor library @ ^1.4.6
    adafruit/Adafruit Unified Sensor @ ^1.1.14
```

```cpp
#include <Arduino.h>
#include <DHT.h>

#define DHTPIN 4         // GPIO-pin tilsluttet sensoren
#define DHTTYPE DHT11    // Sættes til DHT11 (eller DHT22)

DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(115200);
    dht.begin();
    Serial.println("DHT11 sensor initialiseret!");
}

void loop() {
    delay(2000); // Vent 2 sekunder mellem målinger

    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature(); // Målt i Celsius

    // Kontroller om læsningen fejlede (read returnerer 'nan')
    if (isnan(humidity) || isnan(temperature)) {
        Serial.println("Kunne ikke læse fra DHT-sensoren! Tjek forbindelser.");
        return;
    }

    Serial.print("Luftfugtighed: ");
    Serial.print(humidity);
    Serial.print(" %  |  ");
    Serial.print("Temperatur: ");
    Serial.print(temperature);
    Serial.println(" C");
}
```

---

## Typiske fejl og eksamensspørgsmål
- **Sensoren returnerer `nan`**: Dette er den mest almindelige fejl. Det betyder, at timingen i signalet slog fejl, eller at sensoren er forkert forbundet. Tjek strøm, fælles GND og GPIO pin-nummer.
- **Hvorfor er der delay?**: DHT11 har en indbygget langsom målesyklus. Læser man den for hurtigt, fejler kommunikationen.
- **Digital vs. Analog**: DHT11 er en digital sensor. ESP32'erens ADC er ikke involveret her; protokollen afkodes direkte i softwaren.
