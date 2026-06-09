# Sensoroversigt

```text
Sensor          Måler                         Signal/interface
DHT11           temperatur + fugtighed         digital data pin
BMP280          tryk + temperatur              I2C/SPI
MQ-135          gas/luftkvalitet               analog spænding
LDR             lysniveau                      analog spænding via spændingsdeler
MPU6050/GY-521  acceleration + rotation        I2C
HMC5883L/GY-271 magnetfelt/kompas              I2C
ADS1115         ekstern analog måling          I2C
DS18B20         temperatur                     OneWire digital bus
```

God eksamensvinkel:

> Først forklarer jeg hvad sensoren fysisk måler. Derefter forklarer jeg hvilket signal ESP32 modtager, fx analog spænding, I2C-data eller OneWire-data. Til sidst forklarer jeg hvordan rå data bliver til en brugbar værdi i koden.
