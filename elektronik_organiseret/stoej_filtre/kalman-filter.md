# Avanceret softwarefilter: Kalman-filter

I emneoversigten nævnes Kalman-filteret under filtrering og sensor-fusion:
- **Hvad er det**: En matematisk algoritme, der estimerer den sande tilstand af et system ud fra en række støjfyldte målinger over tid.
- **Anvendelse**: Typisk til sensor-fusion, fx i droner eller balance-robotter. Her kombinerer man accelerometer-data (som reagerer hurtigt, men er støjfyldte pga. vibrationer) med gyroskop-data (som er rolige på kort sigt, men driver/drifter over tid). Kalman-filteret vægter de to sensorer optimalt for at beregne den præcise vinkel.
- **Konceptuelt flow (rekursivt)**:
  1. **Predict (Forudsig)**: Estimer den næste tilstand ud fra en fysisk model af systemet.
  2. **Update (Opdater)**: Mål med sensorerne, beregn usikkerheden (Kalman Gain), og korriger forudsigelsen med målingen.

---
