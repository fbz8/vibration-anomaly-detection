wn = 2;
zetas = [0.2 0.7 1];
t = linspace(0, 10, 2001)';
figure; hold on;
for zeta = zetas
    f = @(t, x) [x(2); -wn^2*x(1) - 2*zeta*wn*x(2) + wn^2];   % unit step input
    [tt, x] = ode45(f, t, [0; 0]);
    y = x(:, 1);
    plot(tt, y, 'LineWidth', 1.3);
    os = max(max(y) - 1, 0)*100;
    fprintf('zeta = %.1f: overshoot = %.1f %% (formula: %.1f %%), poles: ', ...
        zeta, os, 100*exp(-pi*zeta/sqrt(1 - zeta^2)));
    disp(roots([1 2*zeta*wn wn^2]).');
end
yline(1, '--'); grid on; xlabel('Time (s)'); ylabel('Output');
legend('zeta = 0.2', 'zeta = 0.7', 'zeta = 1');