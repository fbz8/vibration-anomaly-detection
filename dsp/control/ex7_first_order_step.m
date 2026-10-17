taus = [0.5 1 2];
t = linspace(0, 12, 1201)';
figure; hold on;
for tau = taus
    [tt, y] = ode45(@(t, y) (-y + 1)/tau, t, 0);   % unit step input
    plot(tt, y, 'LineWidth', 1.3);
    t10 = tt(find(y >= 0.1, 1));
    t90 = tt(find(y >= 0.9, 1));
    idx = find(abs(y - 1) > 0.02, 1, 'last');
    ts  = tt(idx + 1);
    fprintf('tau = %.1f: rise time = %.2f s (2.2*tau = %.2f), settling (2%%) = %.2f s (4*tau = %.2f)\n', ...
        tau, t90 - t10, 2.2*tau, ts, 4*tau);
end
grid on; xlabel('Time (s)'); ylabel('Output');
legend('tau = 0.5', 'tau = 1', 'tau = 2');