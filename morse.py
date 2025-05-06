import numpy as np
from scipy.io import wavfile

# Morse kod tablosu
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C',
    '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I',
    '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U',
    '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5',
    '-....': '6', '--...': '7', '---..': '8',
    '----.': '9'
}

# Ses dosyasını oku
rate, data = wavfile.read("C://Users//Lenovo//Downloads//budane.wav")

# Stereo ise mono'ya çevir
if len(data.shape) > 1:
    data = data[:, 0]

# Normalize et
data = data / np.max(np.abs(data))

# Mutlak değer al → sinyalin gücü
amplitude = np.abs(data)

# Eşik belirle (beep varsa)
threshold = 0.1
is_beep = amplitude > threshold

# Zaman hesapla
duration = len(data) / rate
time_step = 1 / rate
timestamps = np.arange(0, duration, time_step)

# Beep/sessizlik sürelerini analiz et
durations = []
current = is_beep[0]
count = 0

for i in is_beep:
    if i == current:
        count += 1
    else:
        durations.append((current, count))
        current = i
        count = 1

# Son bloğu ekle
durations.append((current, count))

# Nokta/tire/sessizlikleri çöz
morse = ""
unit = rate * 0.1  # 0.1 saniye = temel birim

for is_tone, length in durations:
    if is_tone:
        if length < unit * 1.5:
            morse += "."
        else:
            morse += "-"
    else:
        if length > unit * 6:
            morse += " / "   # kelime arası
        elif length > unit * 2:
            morse += " "     # harf arası

# Morse'u yaz
print("[Morse]:", morse)

# Morse'u harfe çevir
message = ""
for word in morse.split(" / "):
    for char in word.strip().split(" "):
        if char in MORSE_CODE_DICT:
            message += MORSE_CODE_DICT[char]
        else:
            message += '?'
    message += " "

print("[Çözülmüş Mesaj]:", message.strip())
