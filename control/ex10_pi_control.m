tau = 1; Kp = 4; Ki_list = [1 4 25];
t = linspace(0, 25, 2501)';
figure; hold on;
for Ki = Ki_list
    % states: x(1) = output y, x(2) = integral of the error
    f = @(t, x) [(-x(1) + Kp*(1 - x(1)) + Ki*x(2))/tau; 1 - x(1)];
    [tt, x] = ode45(f, t, [0; 0]);
    y = x(:, 1);
    plot(tt, y, 'LineWidth', 1.3);
    os = max(max(y) - 1, 0)*100;
    idx = find(abs(y - 1) > 0.02, 1, 'last'); ts = tt(idx + 1);
    fprintf('Ki = %2d: final value = %.3f, overshoot = %.1f %%, settling time = %.2f s\n', Ki, y(end), os, ts);
end
yline(1, '--'); grid on; xlabel('Time (s)'); ylabel('Output');
legend('Ki = 1', 'Ki = 4', 'Ki = 25');