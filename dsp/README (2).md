# DSP Exercises (MATLAB)

Short signal-processing exercises I did while building the [vibration anomaly detection project](../README.md). Each script is self-contained, uses core MATLAB only (no toolboxes) and was run in MATLAB Online. All signals are simulated (sampling rate fs = 100 Hz).

## Exercises

| File | Topic | What I found |
|---|---|---|
| `ex1_fft_windows.m` | FFT of a 5.5 Hz sine (N = 100): rectangular window vs Hann window vs Hann + zero-padding | FFT bins are fs/N = 1 Hz apart. A tone between bins loses amplitude with a rectangular window (peak about 0.66 instead of 1.0) and leaks into other frequencies. Hann reduces leakage (peak about 0.9). Zero-padding to 1024 points places the peak at 5.5 Hz. With the tone exactly on a bin (5 Hz), the rectangular window gives a clean spike. |
| `ex2_two_tone.m` | Spectrum of a 5 Hz + 12 Hz signal with noise | Both tones show up at the right frequencies, with the 12 Hz peak at about half the amplitude, as expected. Resolution is set by window length (fs/N), not by zero-padding. Two tones 0.5 Hz apart would merge at N = 100 (expected from theory, not run here). |
| `ex3_aliasing_moving_average.m` | Aliasing and a moving-average filter | A 70 Hz tone sampled at 100 Hz appears at 30 Hz (\|70 - 100\|). A moving average with M = 5 has gain 0.904 at 5 Hz and about 0.25 at 30 Hz, with zeros every fs/M = 20 Hz and a delay of (M-1)/2 samples (20 ms). With M = 10 the 30 Hz tone is removed but the wanted 5 Hz signal drops to about 0.64 and the delay grows to 45 ms. |
| `ex4_fir_lowpass.m` | Windowed-sinc FIR low-pass (fc = 10 Hz, L = 31, Hann window) | About -70 dB at 30 Hz, compared with about -12 dB for the M = 5 moving average. Delay (L-1)/2 = 15 samples = 0.15 s. The transition width is roughly 3 x fs/L (about 10 Hz here), so a sharper filter needs more taps and adds more delay. |

## How this connected to the project

- The first version of the detector had 1 Hz FFT bins, so `dominant_freq` could not see small frequency shifts (5.2 Hz was detected in 1% of windows). Applying what I learned in exercise 1 (Hann window + zero-padding to 1024 points) raised detection of a 0.2 Hz shift to 97% on simulated data, with no change in false alarms.
- Exercises 3 and 4 explain why a real sensor such as the MPU6050 needs its low-pass filter set below fs/2 before sampling: aliasing cannot be removed after sampling.

## Key takeaways

1. Frequency resolution is fs/N. More samples (a longer window) improve resolution; zero-padding only interpolates.
2. A window function trades main-lobe width for lower leakage.
3. A tone above fs/2 folds back as a false lower frequency, and it cannot be removed afterwards.
4. Every filter trades sharpness against delay and length.

## Next

- Spectrogram of the normal and abnormal vibration data
- Simulink basics and a simple control loop
