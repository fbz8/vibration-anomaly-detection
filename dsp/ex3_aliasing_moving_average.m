fs = 100; N = 300; t = (0:N-1)'/fs;
w = 0.5*(1 - cos(2*pi*(0:N-1)'/(N-1)));
Nfft = 2048; f = (0:Nfft-1)'*fs/Nfft;
spec = @(s) 2*abs(fft(s.*w, Nfft))/sum(w);

% Part A: aliasing (70 Hz tone sampled at 100 Hz)
xa = sin(2*pi*70*t);
Xa = spec(xa);

% Part B: moving-average filter
x = sin(2*pi*5*t) + 0.5*sin(2*pi*30*t) + 0.2*randn(N,1);
M = 10;
h = ones(M,1)/M;
y = filter(h, 1, x);
X = spec(x); Y = spec(y);
H = abs(fft(h, Nfft));

figure;
subplot(2,2,1); plot(f(1:Nfft/2), Xa(1:Nfft/2)); xlim([0 50]); grid on;
title('A: 70 Hz sine sampled at 100 Hz'); xlabel('Hz');

subplot(2,2,2); plot(f(1:Nfft/2), H(1:Nfft/2)); xlim([0 50]); grid on;
title(sprintf('B: moving average (M=%d) gain', M)); xlabel('Hz');

subplot(2,2,3); plot(t, x, t, y); xlim([0 1]); grid on;
legend('input', 'filtered'); title('time domain'); xlabel('s');

subplot(2,2,4);
plot(f(1:Nfft/2), X(1:Nfft/2), f(1:Nfft/2), Y(1:Nfft/2)); xlim([0 50]); grid on;
legend('input', 'filtered'); title('spectrum'); xlabel('Hz');