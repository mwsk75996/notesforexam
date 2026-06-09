# I2C detaljer på ESP32

I2C (Inter-Integrated Circuit) bruges til at forbinde mange sensorer på de samme to ledninger. Hver enhed har en unik hex-adresse (fx `0x3C` eller `0x76`).

Eksempler på I2C-enheder:
- **BMP280** tryk/temperatur (typisk adresse `0x76` eller `0x77`)
- **Display OLED 1.3”** (typisk adresse `0x3C`)
- **GY-521 MPU6050** accelerometer/gyro (typisk adresse `0x68`)
- **ADS1115** ekstern ADC (typisk adresse `0x48`)

### Hvorfor Pull-up modstande på I2C?
I2C-bussen bruger "open-drain" udgange. Det betyder, at enhederne kun kan trække signalet aktivt **LOW** (til GND). De kan ikke tvinge linjen HIGH. Derfor skal der være eksterne **pull-up modstande** (fx $4.7\text{ k}\Omega$) til $3.3\text{V}$ på både `SDA` og `SCL`. Uden dem vil signalet forblive LOW, og kommunikationen fejler. De fleste sensor-breakoutboards har disse modstande indbygget.

---
