# Vibration Anomaly Detection (Simulated Sensor Data)

A small predictive-maintenance prototype: simulate accelerometer-style vibration data, extract signal features, and train a model on **healthy data only** to flag abnormal vibration.

> **Important:** all data in this project is **simulated** (sine wave + Gaussian noise). No physical sensor data was used yet. Planned hardware: MPU6050 + Arduino Nano, with the circuit designed in KiCad.

## Pipeline

1. `sensor_data.py` creates `normal.csv` and `abnormal.csv` (100 Hz sampling, 50,000 rows each).
   - Normal: 5 Hz sine, amplitude 1.0, noise sigma 0.3
   - Abnormal: 12 Hz sine, amplitude 3.0, noise sigma 0.8
2. `detect.py` cuts the signal into 1-second windows (50% overlap) and extracts 4 features per window: RMS, variance, peak, dominant frequency (FFT).
3. A One-Class SVM is trained on the first half of the normal windows only, then tested on unseen normal windows and on abnormal windows.

## Results

| Setting | False alarms (normal flagged) | Detection (abnormal flagged) |
|---|---|---|
| Isolation Forest, 2,000 rows | 0% | **0%** |
| One-Class SVM (scaled), 10,000 rows, gamma="scale" | ~17% | 100% |
| One-Class SVM, gamma=0.03, nu=0.02, 10,000 rows | ~8% | 100% |
| One-Class SVM, gamma=0.03, nu=0.02, 50,000 rows | ~2-4% | 100% |

### What I learned
- **Isolation Forest failed completely (0% detection).** My best explanation: the abnormal windows lie far outside the range of the training data on every feature, so random cuts do not separate them from the extreme training points. Isolation Forest is better at finding outliers inside the data cloud than far outside it.
- **A scaled One-Class SVM fixed detection.** It measures distance from the learned "normal" region.
- **Lowering `gamma` and adding data reduced false alarms** from about 17% to about 2-4%. More data helped more than parameter tuning.

### Detection limit (subtler faults)

Amplitude change only (frequency fixed at 5 Hz):

| Amplitude vs. normal | Detected |
|---|---|
| +5% | 6% |
| +10% | 31% |
| +15% | 76% |
| +20% | 96% |
| +30% | 100% |

Frequency change only (amplitude fixed at 1.0):

| Frequency | Detected |
|---|---|
| 5.1 Hz | 2% |
| 5.2 Hz | 1% |
| 5.5 Hz | 2% |
| 6 Hz | 3% |
| 7 Hz | 32% |

With a false alarm rate of about 2%, detection of 1-3% is indistinguishable from noise.

## Limitations
- The model reliably detects amplitude increases of roughly 20% or more, but **barely detects frequency shifts** below about 2 Hz.
- Hypothesis (not tested): 1-second windows give only 1 Hz FFT resolution, and `dominant_freq` has almost no variance in the training data. Zero-padding the FFT or using longer windows are untested next steps.
- Results are on simulated data with one fault type. Real machine vibration is messier.
- Detection is per window. A real system would likely require several consecutive anomalous windows before raising an alarm.

## Next steps
- Test zero-padded FFT and longer windows for frequency sensitivity
- Add a "3 of the last 5 windows" alarm rule
- Validate on a public bearing vibration dataset (e.g., CWRU)
- Replace simulated data with real MPU6050 readings
- Design the sensor board schematic in KiCad

## Run it
```
pip install numpy pandas scikit-learn
python sensor_data.py
python detect.py
```
