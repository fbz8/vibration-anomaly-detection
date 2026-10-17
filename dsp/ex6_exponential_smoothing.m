fs = 100; N = 300; t = (0:N-1)'/fs;
x = sin(2*pi*5*t) + 0.5*randn(N,1);      % 5 Hz signal + strong noise
alphas = [0.5 0.8 0.95];

figure; hold on;
plot(t, x, 'Color', [0.7 0.7 0.7]);
for a = alphas
    y = filter(1-a, [1 -a], x);          % y[n] = a*y[n-1] + (1-a)*x[n]
    plot(t, y, 'LineWidth', 1.3);
end
xlim([0 1.5]); grid on; xlabel('Time (s)');
legend('input', 'a = 0.5', 'a = 0.8', 'a = 0.95');

Nfft = 2048; f = (0:Nfft-1)'*fs/Nfft;
figure; hold on;
for a = alphas
    H = abs(fft([1-a; 0], Nfft) ./ fft([1; -a], Nfft));
    plot(f(1:Nfft/2), H(1:Nfft/2));
end
xlim([0 50]); grid on; xlabel('Frequency (Hz)'); ylabel('Gain');
legend('a = 0.5', 'a = 0.8', 'a = 0.95');