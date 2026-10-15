fs = 100; N = 300; t = (0:N-1)'/fs;
x = sin(2*pi*5*t) + 0.5*sin(2*pi*30*t) + 0.2*randn(N,1);

% Windowed-sinc low-pass FIR
fc = 10;                     % cutoff (Hz)
L  = 31;                     % filter length (odd)
n  = (0:L-1)' - (L-1)/2;     % centered index
wc = fc/(fs/2);              % cutoff relative to Nyquist
arg = wc*n;
h  = wc * (sin(pi*arg) ./ (pi*arg));
h((L+1)/2) = wc;             % fix 0/0 at the center
win = 0.5*(1 - cos(2*pi*(0:L-1)'/(L-1)));
h = h .* win;
h = h / sum(h);              % unity gain at 0 Hz

% Moving average for comparison
hm = ones(5,1)/5;

Nfft = 2048; f = (0:Nfft-1)'*fs/Nfft;
H1 = abs(fft(h,  Nfft));
H2 = abs(fft(hm, Nfft));

y = filter(h, 1, x);

figure;
subplot(2,2,1);
plot(f(1:Nfft/2), H1(1:Nfft/2), f(1:Nfft/2), H2(1:Nfft/2)); xlim([0 50]); grid on;
legend('windowed-sinc', 'moving avg'); title('gain'); xlabel('Hz');

subplot(2,2,2);
plot(f(1:Nfft/2), 20*log10(H1(1:Nfft/2)+eps), f(1:Nfft/2), 20*log10(H2(1:Nfft/2)+eps));
xlim([0 50]); ylim([-80 5]); grid on;
legend('windowed-sinc', 'moving avg'); title('gain (dB)'); xlabel('Hz');

subplot(2,1,2);
plot(t, x, t, y); xlim([0 1.5]); grid on;
legend('input', 'filtered'); title('time domain'); xlabel('s');