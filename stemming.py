#%%
import numpy as np
import pandas as pd
import re
from collections import Counter

# %% Tokenizing
def tokenizing(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    return text

#%% Stopword
def stop_word(word):
    with open('stopwords-id.txt', encoding='utf-8') as f:
        s_word = f.read().splitlines()
    if word not in s_word:
        return word
    return None

#%% LKamus Kata Dasar
AKAR_KATA = []
kamus_clean = []
def load_dictionary():
    global kamus_clean
    with open('kata-dasar.txt', encoding='utf-8') as f:
        content = f.read()
        content = re.sub(r'[^\w\s]', ' ', content)
        words = re.findall(r'\b\w+\b', content.lower())
        kamus_clean = [w for w in words if w]

load_dictionary()

def kamus_word(word):
    global AKAR_KATA
    if not word:
        return None
    
    if word in kamus_clean:
        if word not in AKAR_KATA:
            AKAR_KATA.append(word)
        return None
    return word

#%% Load inflectional suffixes dan prefix data
inflectional_suffixes = ['lah', 'kah', 'tah', 'pun']
possessive_pronoun_suffixes = ['ku', 'mu', 'nya']
derivational_suffixes = ['i', 'kan', 'an']
derivational_prefixes = ['di', 'ke', 'se', 'be', 'me', 'pe', 'te']

forbidden_prefixes = ['mepe', 'memper', 'beke']  # contoh kombinasi prefix yang dilarang
checked_prefixes = []

#%% Fungsi utama Nazief Stemming
def nazief_stem(word):
    original_word = word
    word = kamus_word(word)
    if word is None:
        return original_word

    for suf in inflectional_suffixes + possessive_pronoun_suffixes:
        if word.endswith(suf):
            temp = word[:-len(suf)]
            word = temp if kamus_word(temp) else word
            break

    for suf in derivational_suffixes:
        if word.endswith(suf):
            temp = word[:-len(suf)]
            word = temp if kamus_word(temp) else word
            break

    result = remove_prefixes(word, 0)
    if result:
        return result

    # Final check: return akar kata jika tersedia
    return AKAR_KATA[-1] if AKAR_KATA else word


#%% Fungsi bantu hapus prefix
def remove_prefixes(word, count):
    if count >= 3:
        return None
    
    for pre in derivational_prefixes:
        if word.startswith(pre):
            temp = word[len(pre):]
            
            # Cek kombinasi dilarang
            if any(temp.startswith(fp) for fp in forbidden_prefixes):
                return None

            # Cek duplikasi prefix
            if pre in checked_prefixes:
                continue

            checked_prefixes.append(pre)

            # Penanganan langsung untuk {di, ke, se}
            if pre in ['di', 'ke', 'se']:
                if kamus_word(temp) is None:
                    return AKAR_KATA[-1] if AKAR_KATA else temp

            # Untuk {be, te, me, pe}, dicek sesuai tabel aturan (di sini di-simplifikasi)
            else:
                if kamus_word(temp) is None:
                    return AKAR_KATA[-1] if AKAR_KATA else temp

                # Rekursif: coba hapus prefix lagi
                result = remove_prefixes(temp, count + 1)
                if result:
                    return result
    return None

#%% Contoh Preprocessing dan Stemming
def preprocess_and_stem(text):
    tokens = tokenizing(text).lower().split()
    print("Tokens:", tokens)
    hasil = []
    for word in tokens:
        word = stop_word(word)
        print(f"{word} -> after stopword check: {word}")
        if word:
            AKAR_KATA.clear()
            checked_prefixes.clear()
            akar = nazief_stem(word)
            hasil.append(akar)
    return hasil

#%% Simpan hasil stemming ke file CSV
def simpan_hasil_stemming(teks_input, nama_file='hasil_stemming.csv'):
    tokens = tokenizing(teks_input).lower().split()
    hasil_data = []

    for word in tokens:
        cleaned = stop_word(word)
        if cleaned:
            AKAR_KATA.clear()
            checked_prefixes.clear()
            hasil = nazief_stem(cleaned)
            print(f"Stemming: {cleaned} -> {hasil}")
            hasil_data.append({
                'kata_awal': cleaned,
                'kata_stemming': hasil
            })

    df = pd.DataFrame(hasil_data)
    df.to_csv(nama_file, index=False, encoding='utf-8')
    print(f"Hasil stemming disimpan di: {nama_file}")

if __name__ == "__main__":
    with open("dokumen Bahasa Indonesia.txt", encoding='utf-8') as file:
        teks = file.read()
    
    simpan_hasil_stemming(teks)

