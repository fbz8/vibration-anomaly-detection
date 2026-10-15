fs = 100;                 % sampling frequency (Hz)
N  = 100;                 % window length (1 second)
f0 = 5;                 % signal frequency, deliberately between bins
t  = (0:N-1)'/fs;
x  = 1.0*sin(2*pi*f0*t) + 0.3*randn(N,1);

% 1) Rectangular window (no window)
w1 = ones(N,1);
X1 = 2*abs(fft(x.*w1))/sum(w1);
f1 = (0:N-1)'*fs/N;

% 2) Hann window
w2 = 0.5*(1 - cos(2*pi*(0:N-1)'/(N-1)));
X2 = 2*abs(fft(x.*w2))/sum(w2);

% 3) Hann window + zero padding to 1024 points
Nfft = 1024;
X3 = 2*abs(fft(x.*w2, Nfft))/sum(w2);
f3 = (0:Nfft-1)'*fs/Nfft;

figure;
plot(f1(1:N/2), X1(1:N/2), 'o-', ...
    f1(1:N/2), X2(1:N/2), 's-', ...
    f3(1:Nfft/2), X3(1:Nfft/2), '-', 'LineWidth', 1.2);
xlim([0 20]); grid on;
xlabel('Frequency (Hz)'); ylabel('Amplitude');
legend('Rectangular', 'Hann', 'Hann + zero-pad');
title('FFT of a 5.5 Hz sine, 1-second window');