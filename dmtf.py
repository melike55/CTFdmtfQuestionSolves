import numpy as np
import scipy.io.wavfile as wav
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# DTMF frekansları ve karşılıkları
DTMF_TONES = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#'
}

# WAV dosyasını oku
rate, data = wav.read("budane.wav")

# Eğer stereo sesse mono'ya çevir
if len(data.shape) > 1:
    data = data[:, 0]

# Ses dosyasının boyutunu kontrol et
duration = len(data) / rate
print(f"Dosya süresi: {duration:.2f} saniye")

# FFT işlemi ile frekansları çıkart
def get_frequencies(data, rate):
    n = len(data)
    freqs = fftfreq(n, 1/rate)
    fft_data = fft(data)
    
    # Pozitif frekansları seç
    positive_freqs = freqs[:n//2]
    positive_fft = np.abs(fft_data[:n//2])
    
    return positive_freqs, positive_fft

# DTMF çözümü için frekansları çöz
def detect_dtmf(positive_freqs, positive_fft):
    dtmf_detected = []
    
    for (f1, f2) in DTMF_TONES.keys():
        # İki frekansı bulmaya çalışıyoruz
        idx1 = np.argmin(np.abs(positive_freqs - f1))
        idx2 = np.argmin(np.abs(positive_freqs - f2))
        
        # Her iki frekansın genliğini al
        if positive_fft[idx1] > 0.5 and positive_fft[idx2] > 0.5:
            dtmf_detected.append(DTMF_TONES[(f1, f2)])
    
    return ''.join(dtmf_detected)

# Frekansları al
positive_freqs, positive_fft = get_frequencies(data, rate)

# DTMF tonlarını çöz
message = detect_dtmf(positive_freqs, positive_fft)

print("Çözülmüş DTMF Mesajı:", message)
