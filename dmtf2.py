import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

# Ses dosyasını oku
samplerate, data = wavfile.read('budane.wav')

# Eğer stereo bir ses dosyası ise, sadece tek bir kanal al (mono)
if len(data.shape) > 1:
    data = data[:, 0]

# Zaman ekseninde sesin dalga formunu çiz
plt.figure(figsize=(10, 6))
plt.plot(np.linspace(0, len(data) / samplerate, num=len(data)), data)
plt.title("Ses Dalga Formu")
plt.xlabel("Zaman (saniye)")
plt.ylabel("Genlik")
plt.grid(True)
plt.show()

# Spektrogramı çiz
f, t, Sxx = spectrogram(data, samplerate)

# Spektrogramı görselleştir
plt.figure(figsize=(10, 6))
plt.pcolormesh(t, f, np.log(Sxx), shading='auto')
plt.title("Spektrogram")
plt.xlabel("Zaman (saniye)")
plt.ylabel("Frekans (Hz)")
plt.colorbar(label='Log Genlik')
plt.grid(True)
plt.show()
