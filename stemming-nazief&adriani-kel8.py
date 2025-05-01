#%% Import Librray
import re
from collections import Counter
from itertools import combinations
from statistics import mean

#%% Tokenizing
def tokenizing(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    return text

#%% Menghapus Stopwords
stopwords = set()

def load_stopwords(file_path='stopwords-id.txt'):
    global stopwords
    with open(file_path, encoding='utf-8') as f:
        stopwords = set(word.strip().lower() for word in f if word.strip())

def remove_stopwords(tokens):
    return [word for word in tokens if word not in stopwords]

#%% Load Kamus Kata Dasar
kamus_kata_dasar = set()

def load_kamus(file_path='kata-dasar.txt'):
    global kamus_kata_dasar
    with open(file_path, encoding='utf-8') as f:
        kamus_kata_dasar = set(word.strip().lower() for word in f if word.strip())

#%% Mengganti Suffix dan Prefix
def simple_stem(word):
    if word in kamus_kata_dasar:
        return word

    for suf in ['lah', 'kah', 'pun', 'ku', 'mu', 'nya', 'kan', 'an', 'i']:
        if word.endswith(suf):
            base = word[:-len(suf)]
            if base in kamus_kata_dasar:
                return base
            word = base

    for pre in ['meng', 'meny', 'men', 'mem', 'me', 'peng', 'peny', 'pen', 'pem', 'pe', 'ber', 'be', 'ter', 'se', 'di', 'ke']:
        if word.startswith(pre):
            base = word[len(pre):]
            if base in kamus_kata_dasar:
                return base

    return word

#%% Stemming
def proses_stemming(input_file='dokumen Bahasa Indonesia.txt', output_file='hasil_stemming.txt'):
    with open(input_file, encoding='utf-8', errors='ignore') as f:
        text = f.read()
        processed_text = tokenizing(text)
        tokens = processed_text.split()
        tokens = remove_stopwords(tokens)
        stems = [simple_stem(word) for word in tokens]

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(' '.join(stems))
    print(f"Hasil stemming disimpan ke {output_file}")
    return tokens, stems

# Golden Standard
def golden_standard(tokens, stems, output_file='golden_standard.csv'):
    pairs = []
    for original, stem in zip(tokens, stems):
        pairs.append((original, stem))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('kata_asli,kata_stemmed\n')
        for word, stem in pairs:
            f.write(f'{word},{stem}\n')
    print(f"✓ Golden standard disimpan ke {output_file}")
    return pairs

#%% Evaluasi Menggunakan UI, OI, dan MWC
def evaluasi_stemming(golden_standard, original_tokens, hasil_stem):
    # Menghitung UI
    N_total_ui = len(golden_standard)
    N_under = 0
    for w1, w2 in golden_standard:
        if simple_stem(w1) != simple_stem(w2):
            N_under += 1
    UI = N_under / N_total_ui if N_total_ui else 0

    # Menghitung OI
    N_total_oi = len(golden_standard)
    N_over = 0
    for w1, w2 in golden_standard:
        if simple_stem(w1) == simple_stem(w2):
            N_over += 1
    OI = N_over / N_total_oi if N_total_oi else 0

    # Menghitung MWC
    N_total = len(original_tokens)
    roots = set([simple_stem(w) for w in original_tokens])
    N_roots = len(roots)
    MWC = N_total / N_roots if N_roots else 0

    return UI, OI, MWC

#%% Main
if __name__ == "__main__":
    load_kamus()
    load_stopwords()
    tokens_asli, hasil_stem = proses_stemming()
    golden_standard = golden_standard(tokens_asli, hasil_stem)

    ui, oi, mwc = evaluasi_stemming(golden_standard, tokens_asli, hasil_stem)
    print("\n--- HASIL EVALUASI ---")
    print(f"Under-stemming Index (UI): {ui:.4f}")
    print(f"Over-stemming Index (OI): {oi:.4f}")
    print(f"Mean Word Conflation (MWC): {mwc:.4f}")
