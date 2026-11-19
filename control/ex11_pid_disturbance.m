% ex11_pid_disturbance.m - P vs PI vs PID on a second-order plant, step disturbance at t = 15 s
wn = 2; zeta = 0.2; r = 1; d0 = 0.5; td = 15;
gains = [2 0 0; 2 1 0; 2 1 1];      % rows: [Kp Ki Kd]
names = {'P', 'PI', 'PID'};
t = linspace(0, 30, 3001)';
figure; hold on;
for k = 1:3
    Kp = gains(k,1); Ki = gains(k,2); Kd = gains(k,3);
    % states: x(1) = y, x(2) = dy/dt, x(3) = integral of the error
    % D acts on the measurement (-Kd*dy/dt), so a setpoint step gives no derivative kick
    f = @(t, x) [x(2); ...
        -2*zeta*wn*x(2) - wn^2*x(1) + wn^2*(Kp*(r - x(1)) + Ki*x(3) - Kd*x(2) + d0*(t >= td)); ...
        r - x(1)];
    [tt, x] = ode45(f, t, [0; 0; 0], odeset('MaxStep', 0.01));
    y = x(:, 1);
    plot(tt, y, 'LineWidth', 1.3);

    before = y(tt >= 14 & tt < 15);                 % just before the disturbance
    yfinal = mean(before(end-50:end));              % the value this controller settles to
    os = max((max(y(tt < td)) - yfinal) / yfinal, 0) * 100;   % step part only
    fprintf('%-3s: settles at %.3f before disturbance, %.3f at t = 30 s, step overshoot = %.1f %%\n', ...
        names{k}, yfinal, y(end), os);
end
xline(td, ':'); yline(1, '--'); grid on; xlabel('Time (s)'); ylabel('Output');
legend('P', 'PI', 'PID');
exportgraphics(gcf, 'pid_disturbance.png');