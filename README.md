# Control Exercises (MATLAB / Simulink)

Step-response and feedback-control exercises from the control part of my learning plan. All systems are simulated.

| File | Topic | What I found |
|---|---|---|
| `ex7_first_order_step.m`, `first_order.slx` | Step response of a first-order system, tau = 0.5, 1, 2 | Measured 10-90% rise time = 1.10, 2.20 and 4.39 s (2.2 tau). 2% settling time = 1.96, 3.91 and 7.83 s, i.e. tau*ln(50) = 3.91 tau, which the usual "4 tau" rule rounds. The output reaches 63.2% of its final value at t = tau. It is the same math as exponential smoothing in `dsp/ex6` (a = e^(-T/tau)). |
| `ex8_second_order.m`, `second_order.slx` | Step response of a second-order system, wn = 2 rad/s, zeta = 0.2, 0.7, 1 | Measured overshoot 52.6% / 4.6% / 0% against the formula's 52.7% / 4.6% / 0%. Poles are -0.4 +/- 1.96j, -1.4 +/- 1.43j and -2 (double). The real part sets how fast the oscillation decays, the imaginary part sets its frequency. zeta of about 0.7 is a good compromise between speed and overshoot. |
| `ex9_p_control.m` | P control of a first-order plant, Kp = 1, 4, 10 | Steady-state error is 1/(1+Kp): 0.500, 0.200 and 0.091. Settling time shrinks as 1/(1+Kp): 1.96, 0.79 and 0.36 s. P alone cannot reach zero error at a reasonable gain, and a very high Kp would amplify noise and hit actuator limits. |
| `ex10_pi_control.m` | PI control, Kp = 4, Ki = 1, 4, 25 | The integrator removes the steady-state error (final value 1.000). Overshoot is 0.0 / 0.1 / 24.5%. The closed loop has a zero at -Ki/Kp, so the ex8 formula underestimates the overshoot (16.3% predicted for Ki = 25). At Ki = 4 the zero cancels a pole and the response is first order (settling 0.98 s). |
| `ex11_pid_disturbance.m` | P, PI and PID on a second-order plant (wn = 2, zeta = 0.2), input disturbance d0 = 0.5 at t = 15 s | P settles at 0.665 and moves to 0.833 after the disturbance, matching Kp/(1+Kp) = 0.667 and (Kp+d0)/(1+Kp) = 0.833. PI and PID return to 1.000: the integrator rejects the disturbance. Step overshoot (before t = 15 s, relative to each controller's own final value): P 69.8%, PI 33.8%, PID 0.0%. PI is still oscillating at t = 15 s, so its "settled" value (0.978) is biased low and its true overshoot is about 31%. D acts on the measurement, which avoids derivative kick and damps the response. |
| `ex12_noisy_sensor.m` | ex11 PID with sensor noise (std 0.02), derivative filter Tf = 0.01 vs 0.1 | Actuator noise std(u) = 1.983 vs 0.240: an 8.3x reduction, matching the high-frequency gain ratio (Kp + Kd/Tf) = 102/12 = 8.5. Output noise std(y) is almost unchanged (0.0153 vs 0.0155): the controller trusts the sensor, so low-frequency noise passes to the output, and no controller filter can remove it. Cost of the stronger filter: overshoot 0.0% to 4.0% (slower D gives less damping). Predicted all three results before running. |

## Figures

**ex7 – First-order step response**
![First-order step response](first_order_step.png)

**ex8 – Second-order step response**
![Second-order step response](second_order_step.png)

**ex9 – P control**
![P control](p_control_step.png)

**ex10 – PI control**
![PI control](pi_control_step.png)

**ex11 – P, PI and PID with a disturbance at t = 15 s**
![PID with disturbance](pid_disturbance.png)

**ex12 – Sensor noise: weak (Tf = 0.01) vs strong (Tf = 0.1) derivative filter**
![PID with sensor noise](ex12_noisy_sensor.png)

## Next
- Phase 3: PLC programming in Siemens TIA Portal (PID_Compact uses the same derivative filter idea)
