
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from sklearn.pipeline import make_pipeline

FS = 100     # Sampling rate in Hz (1 / DT)
WIN = 100    # 1 second per window
STEP = 50    # 50% overlap


def features(w):
    rms = np.sqrt(np.mean(w ** 2))
    var = np.var(w)
    peak = np.max(np.abs(w))

    spectrum = np.abs(np.fft.rfft(w - w.mean()))
    freqs = np.fft.rfftfreq(len(w), d=1 / FS)
    dominant_freq = freqs[np.argmax(spectrum)]

    return [rms, var, peak, dominant_freq]


def make_feature_table(filename):
    x = pd.read_csv(filename)["x"].to_numpy()
    rows = []

    for start in range(0, len(x) - WIN + 1, STEP):
        rows.append(features(x[start:start + WIN]))

    return np.array(rows)


def table_from(x):
    return np.array([
        features(x[s:s + WIN])
        for s in range(0, len(x) - WIN + 1, STEP)
    ])


# Load the original datasets
normal = make_feature_table("normal.csv")
abnormal = make_feature_table("abnormal.csv")

# Train on the first half of normal data only
split = len(normal) // 2
train = normal[:split]
test_normal = normal[split:]

# Create and train the One-Class SVM pipeline
model = make_pipeline(
    StandardScaler(),
    OneClassSVM(kernel="rbf", nu=0.02, gamma=0.03)
)

model.fit(train)

# Evaluate on the original datasets
pred_normal = model.predict(test_normal)
pred_abnormal = model.predict(abnormal)

print(
    "Normal windows correctly accepted:",
    np.mean(pred_normal == 1)
)

print(
    "Abnormal windows correctly flagged:",
    np.mean(pred_abnormal == -1)
)


# Generate synthetic signals for additional experiments
rng = np.random.default_rng(42)
t = np.arange(50000) / FS


def signal(amp, freq, noise=0.3):
    return (
        amp * np.sin(2 * np.pi * freq * t)
        + rng.normal(0, noise, len(t))
    )


# Train the model on a separate synthetic healthy signal
healthy = table_from(signal(1.0, 5))
half = len(healthy) // 2

model.fit(healthy[:half])

print(
    "False alarm rate:",
    np.mean(model.predict(healthy[half:]) == -1)
)


# Test changes in both amplitude and frequency
for amp, freq in [
    (3, 12),
    (2, 8),
    (1.5, 6),
    (1.3, 5.5),
    (1.1, 5.2)
]:
    flagged = np.mean(
        model.predict(table_from(signal(amp, freq))) == -1
    )
    print(f"amp={amp}, freq={freq}: detected {flagged:.0%}")


# Test amplitude changes while frequency stays at 5 Hz
print("--- amplitude only (freq stays 5) ---")

for amp in [1.05, 1.1, 1.15, 1.2, 1.3]:
    flagged = np.mean(
        model.predict(table_from(signal(amp, 5))) == -1
    )
    print(f"amp={amp}: detected {flagged:.0%}")


# Test frequency changes while amplitude stays at 1.0
print("--- frequency only (amp stays 1.0) ---")

for freq in [5.1, 5.2, 5.5, 6, 7]:
    flagged = np.mean(
        model.predict(table_from(signal(1.0, freq))) == -1
    )
    print(f"freq={freq}: detected {flagged:.0%}")