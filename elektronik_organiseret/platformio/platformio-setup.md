# platformio.ini Skabelon (ESP32 Wroom 38-Pin)

Konfiguration til PlatformIO-projektet til eksamen. Lægger biblioteker ind automatisk.

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino

; Serial Monitor indstillinger
monitor_speed = 115200
monitor_filters = esp32_exception_decoder

; Biblioteks-afhængigheder (installeres automatisk ved compile)
lib_deps =
    olikraus/U8g2 @ ^2.35.19             ; Til 1.3" SH1106 OLED display
    knolleary/PubSubClient @ ^2.8        ; Til MQTT kommunikation
    milesburton/DallasTemperature @ ^3.9.0 ; Til DS18B20 temp (hvis relevant)
```

---
