import numpy as np
from scipy.io import wavfile

# Morse kod sözlüğü
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

# Ayarlanabilir parametreler
DOT_DURATION = 0.07      # saniye cinsinden nokta süresi
DASH_DURATION = 0.2      # tire süresi
CHAR_SPACE = 0.2         # harf arası boşluk
WORD_SPACE = 0.5         # kelime arası boşluk
THRESHOLD = 0.05         # sinyal gücü eşik değeri

# WAV dosyasını oku
rate, data = wavfile.read("budane.wav")

# Stereo ise mono'ya çevir
if len(data.shape) > 1:
    data = data[:, 0]

# Normalize et
data = data / np.max(np.abs(data))

# Mutlak değer → sinyal gücü
amplitude = np.abs(data)
is_beep = amplitude > THRESHOLD

# Beep/sessizlik bloklarını tespit et
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
durations.append((current, count))

# Süreleri saniyeye çevirip yaz
print("== Sinyal blokları (debug) ==")
for tone, length in durations:
    saniye = length / rate
    print(f"{'BEEP' if tone else 'Sessizlik'}: {saniye:.3f} s")

# Morse kodunu üret
morse = ""
for is_tone, length in durations:
    saniye = length / rate
    if is_tone:
        if saniye < (DOT_DURATION + DASH_DURATION) / 2:
            morse += "."
        else:
            morse += "-"
    else:
        if saniye >= WORD_SPACE:
            morse += " / "
        elif saniye >= CHAR_SPACE:
            morse += " "

print("\n[Morse]:", morse)

# Morse kodunu yazıya çevir
message = ""
for word in morse.strip().split(" / "):
    for char in word.strip().split(" "):
        message += MORSE_CODE_DICT.get(char, '?')
    message += " "

print("[Çözülmüş Mesaj]:", message.strip())
