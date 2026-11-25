"""
ex15 - Overfitting: when a model memorizes instead of learning
Phase 4, Step 1 (scikit-learn basics)

Same data as ex13/ex14. Four models, each scored with 5-fold cross-validation
on BOTH the training folds and the test fold.
  train >> test  -> the model memorized (overfitting)
  train ~= test  -> the model learned a general rule
"""
import numpy as np
from scipy.stats import kurtosis
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

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

models = {
    "Logistic Regression":          LogisticRegression(max_iter=1000),
    "Decision Tree (no limit)":     DecisionTreeClassifier(random_state=0),
    "Decision Tree (max_depth=2)":  DecisionTreeClassifier(max_depth=2, random_state=0),
    "Random Forest (100 trees)":    RandomForestClassifier(n_estimators=100, random_state=0),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
print(f"{'Model':30s} {'Train':>7s} {'Test':>14s} {'Gap':>7s}")
print("-" * 62)
for name, model in models.items():
    r = cross_validate(model, X, y, cv=cv, return_train_score=True)
    tr, te = r["train_score"].mean(), r["test_score"].mean()
    print(f"{name:30s} {tr:7.3f} {te:7.3f} +/-{r['test_score'].std():.3f} {tr - te:7.3f}")