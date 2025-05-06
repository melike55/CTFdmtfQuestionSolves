import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import find_peaks

# Ses dosyasını oku
samplerate, data = wavfile.read("budane.wav")

# Stereo ise mono'ya çevir
if len(data.shape) > 1:
    data = data[:, 0]

# Sinyalin mutlak değeri (negatif değerlerden kurtul)
data_abs = np.abs(data)

# Tepe noktalarını bul
peaks, properties = find_peaks(data_abs, height=1000, distance=samplerate * 0.1)

# Tepe noktalarının genlik değerlerini al
peak_heights = properties["peak_heights"]

# Sayısal olarak yazdır
print("Bulunan bip seslerinin genlik değerleri:")
for i, h in enumerate(peak_heights):
    print(f"Bip {i+1}: Genlik = {int(h)}")
