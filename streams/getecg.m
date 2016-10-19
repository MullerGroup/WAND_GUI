close all
clear all
clc

hdf = h5read('20161018-200157.hdf','/dataGroup/dataTable/');

ch0 = hdf.out(1,:);
ch1 = hdf.out(2,:);
ecg = double(ch1);

Fs = 1000;
Fn = Fs/2;
t = (0:length(ecg)-1)/Fs;
ecg_fft = abs(fft(ecg(20000:20000+1023), 1000));
ecg_fft = ecg_fft(2:501);

figure
subplot(2,1,1)
plot(t, ecg)
subplot(2,1,2)
plot(ecg_fft)

[b,a] = iircomb(round(Fs/60), (60/(Fs/2))/10, 'notch');
filtecg = filtfilt(b,a,ecg);

B = 1/20*ones(20,1);
filtecg = filter(B,1,filtecg);


filt_fft = abs(fft(filtecg(20000:20000+1023), 1000));
filt_fft = filt_fft(2:501);

figure
subplot(2,1,1)
plot(t, filtecg)
subplot(2,1,2)
plot(filt_fft)
