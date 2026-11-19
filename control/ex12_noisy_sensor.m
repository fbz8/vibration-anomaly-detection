% ex12_noisy_sensor.m - ex11 PID with sensor noise: effect of the derivative filter Tf
wn = 2; zeta = 0.2;
G  = tf(wn^2, [1 2*zeta*wn wn^2]);       % same plant as ex11
Kp = 2; Ki = 1; Kd = 1;                   % same PID gains as ex11
Tfs   = [0.01 0.1];                       % weak filter vs strong filter
names = {'Tf = 0.01', 'Tf = 0.1'};

Ts = 0.001; t = (0:Ts:10)';
r  = ones(size(t));
rng(1); n = 0.02*randn(size(t));          % sensor noise, std = 0.02
v  = r - n;                               % the loop sees (r - n)

figure('Position', [100 100 900 600]);
for k = 1:2
    C  = pid(Kp, Ki, Kd, Tfs(k));
    T  = feedback(C*G, 1);                % r -> y
    CS = feedback(C, G);                  % r -> u (actuator command)
    y  = lsim(T, v, t);
    u  = lsim(CS, v, t);
    ss = t > 5;                           % steady-state window
    S  = stepinfo(lsim(T, r, t), t, 1);   % clean step, final value 1
    fprintf('%s | std(u) = %.4f  std(y) = %.5f  overshoot = %.1f %%\n', ...
        names{k}, std(u(ss)), std(y(ss)), S.Overshoot);
    subplot(2,2,k);   plot(t, y); grid on; title(['Output y, ' names{k}]); ylim([0 1.5]);
    subplot(2,2,k+2); plot(t, u); grid on; title(['Actuator u, ' names{k}]);
end
exportgraphics(gcf, 'ex12_noisy_sensor.png');