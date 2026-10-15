fs = 100; N = 100; t = (0:N-1)'/fs;
x = sin(2*pi*5*t) + 0.5*sin(2*pi*12*t) + 0.3*randn(N,1);
w = 0.5*(1 - cos(2*pi*(0:N-1)'/(N-1)));
Nfft = 1024;
X = 2*abs(fft(x.*w, Nfft))/sum(w);
f = (0:Nfft-1)'*fs/Nfft;
plot(f(1:Nfft/2), X(1:Nfft/2)); xlim([0 30]); grid on
xlabel('Frequency (Hz)'); ylabel('Amplitude');