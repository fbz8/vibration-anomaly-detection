# Control Exercises (MATLAB / Simulink)

Step-response exercises from the control part of my learning plan. All systems are simulated.

| File | Topic | What I found |
|---|---|---|
| `ex7_first_order_step.m`, `first_order.slx` | Step response of a first-order system, tau = 0.5, 1, 2 | 10-90% rise time is about 2.2 tau and 2% settling time is about 4 tau. The output reaches 63.2% of its final value at t = tau. It is the same math as exponential smoothing in `dsp/ex6` (a = e^(-T/tau)). |
| `ex8_second_order.m`, `second_order.slx` | Step response of a second-order system, wn = 2 rad/s, zeta = 0.2, 0.7, 1 | Measured overshoot 52.7% / 4.6% / 0% against the formula's 52.7% / 4.6% / 0%. Poles are -0.4 +/- 1.96j, -1.4 +/- 1.43j and -2 (double). The real part sets how fast the oscillation decays, the imaginary part sets its frequency. zeta of about 0.7 is a good compromise between speed and overshoot. |

![Second-order step response](second_order_step.png)

## Next
- Feedback control with P, PI and PID on a simple plant
- Sensor noise and filter delay inside a control loop