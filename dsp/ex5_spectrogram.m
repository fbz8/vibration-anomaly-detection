fs = 100; WIN = 100; STEP = 50; Nfft = 512;
w = 0.5*(1 - cos(2*pi*(0:WIN-1)'/(WIN-1)));
f = (0:Nfft/2)'*fs/Nfft;
files = {'normal.csv', 'abnormal.csv'};

figure;
for i = 1:2
    T = readtable(files{i});
    x = T.x;
    nWin = floor((numel(x) - WIN)/STEP) + 1;
    S = zeros(Nfft/2 + 1, nWin);
    for k = 1:nWin
        seg = x((k-1)*STEP + (1:WIN));
        seg = (seg - mean(seg)) .* w;
        X = abs(fft(seg, Nfft));
        S(:, k) = X(1:Nfft/2 + 1);
    end
    tt = ((0:nWin-1)*STEP + WIN/2)/fs;

    subplot(2,1,i);
    imagesc(tt, f, 20*log10(S + 1e-6));
    axis xy; 
    colorbar; title(files{i});
    xlabel('Time (s)'); ylabel('Frequency (Hz)');
end