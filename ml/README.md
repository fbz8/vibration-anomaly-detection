# Machine Learning Exercises (scikit-learn)

Supervised fault classification on simulated motor vibration, built step by step before moving to real bearing data. All three scripts use the same dataset, so results are directly comparable.

**Dataset (simulated):** 200 one-second signals at 1 kHz, 100 healthy and 100 faulty.
- Healthy: 50 Hz rotation (amplitude 1.0) + Gaussian noise (std 0.5)
- Faulty: the same, plus a weak 120 Hz fault tone (amplitude 0.3)

**Features per signal:** RMS, peak, kurtosis and FFT band energy at 100–150 Hz (Hann window).

## Exercises

| File | Topic | What I found |
|---|---|---|
| `ex13_first_classifier.py` | First supervised classifier: 70/30 train/test split, logistic regression, confusion matrix | Test accuracy 95% (57/60), with 2 false alarms and 1 missed fault. The fault tone (0.3) is weaker than the noise (0.5) overall, but the FFT band holds all of the fault's energy and only about 10% of the noise, so inside the band the fault dominates. Detection limit: fault amplitude 0.5 → 100%, 0.05 → 57% (chance level). |
| `ex14_cross_validation.py` | How reliable is one accuracy number? 10 random splits vs 5-fold cross-validation | The same model on the same data scored anywhere from 90.0% to 98.3% depending only on the split (1 to 6 mistakes in 60). 5-fold CV gives **93.5% ± 2.5%**, so the 95% from ex13 was a lucky split. |
| `ex15_overfitting.py` | Train vs test score for four models (5-fold CV) | See table below. The unlimited decision tree memorized the training data (100%) but scored 90.5% on test. The simplest model won because the fault rule is simple (one threshold on band energy). |

### ex15 results (5-fold cross-validation)

| Model | Train | Test | Gap |
|---|---|---|---|
| Logistic Regression | 0.932 | **0.935 ± 0.025** | −0.003 |
| Decision Tree (no limit) | 1.000 | 0.905 ± 0.056 | 0.095 |
| Decision Tree (max_depth = 2) | 0.953 | 0.905 ± 0.040 | 0.047 |
| Random Forest (100 trees) | 1.000 | 0.925 ± 0.035 | 0.075 |

## Key takeaways

1. **Good features matter more than a clever model.** The FFT band feature (from the `dsp/` exercises) is what makes a weak fault detectable.
2. **Never trust a single train/test split on small data.** Report cross-validated results as mean ± std.
3. **A perfect training score is a warning sign.** A large train–test gap means the model memorized noise. Limiting depth (regularization) or averaging many trees (Random Forest) reduces it.
4. **Start with the simplest model** and add complexity only when cross-validation shows it helps.

## Run it

```
pip install numpy scipy scikit-learn
python ml/ex13_first_classifier.py
python ml/ex14_cross_validation.py
python ml/ex15_overfitting.py
```

All results are from simulated data. Next step: the same workflow on a real bearing-fault dataset (CWRU).