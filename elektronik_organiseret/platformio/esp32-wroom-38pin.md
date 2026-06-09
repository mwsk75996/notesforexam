# ESP32 Wroom 38-Pin Pinout og Hardware-layout

ESP32 Wroom 38-Pin er det specifikke board til eksamen. Det er vigtigt at kende dets pin-grupper:
- **Strømforsyning**:
  - `VIN / 5V`: Ekstern 5V spændingsindgang (eller strøm fra USB-C).
  - `3.3V`: Output fra den indbyggede LDO regulator (må max belastes med ca. 500-800mA til delte sensorer).
  - `GND`: Fælles stel (Ground).
- **Analog Input (ADC)**:
  - **ADC1**: GPIO32-39. **Disse er sikre at bruge når WiFi kører.**
  - **ADC2**: GPIO0, 2, 4, 12-15, 25-27. *Kan IKKE bruges stabilt samtidigt med at WiFi-senderen er aktiv.*
  - **Input-Only Pins**: GPIO34, 35, 36 (VP), 39 (VN) har ingen interne pull-up/pull-down modstande og kan **kun** bruges som input.
- **Kommunikations-pins (Default)**:
  - **I2C**: SDA (GPIO21), SCL (GPIO22).
  - **SPI (VSPI)**: MOSI (GPIO23), MISO (GPIO19), SCLK (GPIO18), CS (GPIO5).
  - **UART0 (USB debug)**: TX (GPIO1), RX (GPIO3).
  - **UART2**: TX2 (GPIO17), RX2 (GPIO16).

---
