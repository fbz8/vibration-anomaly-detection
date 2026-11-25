"""
ex14 - Cross-validation: how much can we trust ONE accuracy number?
Phase 4, Step 1 (scikit-learn basics)

Part A: 10 different random train/test splits -> how much does accuracy jump?
Part B: 5-fold cross-validation -> one honest number: mean +/- std
"""
import numpy as np
from scipy.stats import kurtosis
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(42)

FS, N, N_EACH = 1000, 1000, 100
FAULT_AMP = 0.3
t = np.arange(N) / FS


def make_signal(faulty: bool) -> np.ndarray:
    x = np.sin(2 * np.pi * 50 * t) + 0.5 * rng.standard_normal(N)
    if faulty:
        x += FAULT_AMP * np.sin(2 * np.pi * 120 * t + rng.uniform(0, 2 * np.pi))
    return x


def features(x: np.ndarray) -> list:
    spectrum = np.abs(np.fft.rfft(x * np.hanning(N)))
    freqs = np.fft.rfftfreq(N, 1 / FS)
    band = spectrum[(freqs >= 100) & (freqs <= 150)].sum()
    return [np.sqrt(np.mean(x**2)), np.max(np.abs(x)), kurtosis(x), band]


X = np.array([features(make_signal(bool(lbl))) for lbl in (0, 1) for _ in range(N_EACH)])
y = np.array([lbl for lbl in (0, 1) for _ in range(N_EACH)])

# ---------- Part A: same data, same model, 10 different random splits ----------
print("Part A: one train/test split, repeated with 10 different random seeds")
scores = []
for seed in range(10):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=seed)
    model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
    acc = accuracy_score(y_te, model.predict(X_te))
    scores.append(acc)
    print(f"  split seed {seed}: test accuracy = {acc:.3f}")
print(f"  lowest = {min(scores):.3f}   highest = {max(scores):.3f}")

# ---------- Part B: 5-fold cross-validation ----------
print("\nPart B: 5-fold cross-validation")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
cv_scores = cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=cv)
for i, s in enumerate(cv_scores, 1):
    print(f"  fold {i}: {s:.3f}")
print(f"  RESULT: {cv_scores.mean():.3f} +/- {cv_scores.std():.3f}")
