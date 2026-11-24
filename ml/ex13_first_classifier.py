"""
ex13 - First supervised classifier: healthy vs faulty vibration
Phase 4, Step 1 (scikit-learn basics)

Pipeline:  signals -> features -> train/test split -> model -> evaluate
"""
import numpy as np
from scipy.stats import kurtosis
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

rng = np.random.default_rng(42)   # fixed seed -> same results every run

FS = 1000          # sampling rate [Hz]
N = 1000           # samples per signal (1 second)
N_EACH = 100       # signals per class
FAULT_AMP = 0.3    # strength of the fault tone (try 0.05 later)

t = np.arange(N) / FS


def make_signal(faulty: bool) -> np.ndarray:
    """Motor vibration: 50 Hz rotation + noise. Fault adds a 120 Hz tone."""
    x = np.sin(2 * np.pi * 50 * t) + 0.5 * rng.standard_normal(N)
    if faulty:
        x += FAULT_AMP * np.sin(2 * np.pi * 120 * t + rng.uniform(0, 2 * np.pi))
    return x


def features(x: np.ndarray) -> list:
    """4 numbers that describe one signal."""
    spectrum = np.abs(np.fft.rfft(x * np.hanning(N)))
    freqs = np.fft.rfftfreq(N, 1 / FS)
    band = spectrum[(freqs >= 100) & (freqs <= 150)].sum()   # energy near 120 Hz
    return [np.sqrt(np.mean(x**2)),   # RMS
            np.max(np.abs(x)),        # peak
            kurtosis(x),              # spikiness
            band]                     # fault-band energy


# 1) Build dataset: X = features, y = labels (0 healthy, 1 faulty)
X, y = [], []
for label in (0, 1):
    for _ in range(N_EACH):
        X.append(features(make_signal(faulty=bool(label))))
        y.append(label)
X, y = np.array(X), np.array(y)
print("Dataset shape:", X.shape, "| faulty count:", y.sum())

# 2) Split: model learns on 70%, is graded on 30% it has never seen
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=0)

# 3) Train
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 4) Evaluate
train_acc = accuracy_score(y_train, model.predict(X_train))
test_acc = accuracy_score(y_test, model.predict(X_test))
print(f"Train accuracy: {train_acc:.3f}")
print(f"Test  accuracy: {test_acc:.3f}")
print("Confusion matrix (rows = true, cols = predicted) [healthy, faulty]:")
print(confusion_matrix(y_test, model.predict(X_test)))