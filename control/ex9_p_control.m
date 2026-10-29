tau = 1; Kp_list = [1 4 10];
t = linspace(0, 6, 1201)';
figure; hold on;
for Kp = Kp_list
    f = @(t, y) (-y + Kp*(1 - y))/tau;
    [tt, y] = ode45(f, t, 0);
    plot(tt, y, 'LineWidth', 1.3);
    yss = y(end);
    idx = find(abs(y - yss) > 0.02*yss, 1, 'last'); ts = tt(idx + 1);
    fprintf('Kp = %2d: final value = %.3f, steady-state error = %.3f, settling time = %.2f s\n', Kp, yss, 1 - yss, ts);
end
yline(1, '--'); grid on; xlabel('Time (s)'); ylabel('Output');
legend('Kp = 1', 'Kp = 4', 'Kp = 10');
