#%%
import numpy as np
import pandas as pd
import re
from collections import Counter

# %%
def tokenizing(input):
    input = input.replace(".", "")
    input = input.replace(",", "")
    input = input.replace(":", "")
    input = input.replace("-", " ")
    input = input.replace("?", "")
    input = input.replace("!", "")
    input = input.replace("(", "")
    input = input.replace(")", "")
    input = input.replace("[", "")
    input = input.replace("]", "")
    input = input.replace("{", "")
    input = input.replace("}", "")
    input = input.replace("'", "")
    input = input.replace('"', "")
    input = input.replace("/", "")
    return input

#%% Stopword
def stop_word(word):
    with open('stopwords-id.txt', encoding='utf-8') as f:
        s_word = f.read().splitlines()
    if word not in s_word:
        return word
    return None

#%% Load dictionary (kata dasar)
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

#%% Stemming functions
def hapus_infleksional_suffiks(word):
    """Remove inflectional suffixes"""
    # akhiran -lah, -kah, -nya, -tah, -pun
    if word.endswith('lah') or word.endswith('kah') or word.endswith('nya') or word.endswith('tah') or word.endswith('pun'):
        word = word[0:len(word) - 3]
        word_check = kamus_word(word)
        return word_check

    # akhiran -ku, -mu
    elif word.endswith('ku') or word.endswith('mu'):
        word = word[0:len(word) - 2]
        word_check = kamus_word(word)
        return word_check
    
    return word

def hapus_derivation_suffiks(word):
    """Remove derivational suffixes"""
    # akhiran kan
    if word.endswith('kan'):
        word = word[0:len(word) - 3]
        word_check = kamus_word(word)
        return word_check

    # akhiran i
    if word.endswith('i'):
        word = word[0:len(word) - 1]
        word_check = kamus_word(word)
        return word_check

    # akhiran an
    if word.endswith('an'):
        word = word[0:len(word) - 2]
        word_check = kamus_word(word)
        return word_check
    
    return word

def hapus_derivation_prefiks(word):
    # awalan mempel-
    if (word.startswith('mempel')) and (len(word) > 6):
        sub_word = word[6:]
        word_check = kamus_word(sub_word)
        if word_check != None:
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            return word_check
        return word_check
  
    # awalan memper-
    if (word.startswith('memper')) and (len(word) > 6):
        sub_word = word[6:]
        word_check = kamus_word(sub_word)
        if word_check != None:
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            return word_check
        return word_check

    # awalan diper-, keber-, keter-
    if (word.startswith('diper') or word.startswith('keber') or word.startswith('keter')) and (len(word) > 5):
        sub_word = word[5:]
        word_check = kamus_word(sub_word)
        if word_check != None:
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            return word_check
        return word_check

    # awalan meng-, peng-
    if (word.startswith('meng') or word.startswith('peng')) and (len(word) > 4):
        sub_word = word[4:]
        word_check = kamus_word(sub_word)
        if word_check != None:
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            if word_check != None:
                sub_word = 'k' + word_check
                word_check = kamus_word(sub_word)
                if word_check != None:
                    word_pref_suff_k = hapus_derivation_suffiks(word_check)
                    word_check = kamus_word(word_pref_suff_k)
                    return word_check
        return word_check

    # awalan meny-, peny-
    if (word.startswith('meny') or word.startswith('peny')) and (len(word) > 4):
        sub_word = word[4:]
        word_check = kamus_word(sub_word)
        if word_check != None:  
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            if word_check != None:  
                # add 's' in front word
                sub_word = 's' + word_check
                word_check = kamus_word(sub_word)
                if word_check != None:  
                    word_pref_suff_s = hapus_derivation_suffiks(word_check)
                    word_check = kamus_word(word_pref_suff_s)
                    return word_check
        return word_check

    # awalan mel-, mer-, pel-, per-
    if (word.startswith('mel') or word.startswith('mer') or word.startswith('pel') or word.startswith('per')) and (len(word) > 3):
        sub_word = word[3:]
        word_check = kamus_word(sub_word)
        if word_check != None:  
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            return word_check
        return word_check

    # awalan men-, pen-
    if (word.startswith('men') or word.startswith('pen')) and (len(word) > 3):
        sub_word = word[3:]
        word_check = kamus_word(sub_word)
        if word_check != None:  
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            if word_check != None:  
                # add 't' in front word
                sub_word = 't' + word_check
                word_check = kamus_word(sub_word)
                if word_check != None:  
                    word_pref_suff_t = hapus_derivation_suffiks(word_check)
                    word_check = kamus_word(word_pref_suff_t)
                    return word_check
        return word_check
    
    # awalan mem-, pem-
    if (word.startswith('mem') or word.startswith('pem')) and (len(word) > 3):
        sub_word = word[3:]
        word_check = kamus_word(sub_word)
        if word_check != None:  
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            if word_check != None:  
                # add 'p' in front word
                sub_word = 'p' + word_check
                word_check = kamus_word(sub_word)
                if word_check != None:
                    word_pref_suff_p = hapus_derivation_suffiks(word_check)
                    word_check = kamus_word(word_pref_suff_p)
                    return word_check
        return word_check

    # awalan bel-, ber-, tel-, ter-
    if (word.startswith('bel') or word.startswith('ber') or word.startswith('tel') or word.startswith('ter')) and (len(word) > 3):
        sub_word = word[3:]
        word_check = kamus_word(sub_word)
        if word_check != None:
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            return word_check
        return word_check

    # awalan di-, ke-, se-
    if (word.startswith('di') or word.startswith('ke') or word.startswith('se')) and (len(word) > 2):
        sub_word = word[2:]
        word_check = kamus_word(sub_word)
        if word_check != None:
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            return word_check
        return word_check

    # awalan be-, te-
    if (word.startswith('be') or word.startswith('te')) and (len(word) > 2):
        sub_word = word[2:]
        word_check = kamus_word(sub_word)
        if word_check != None:  
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            return word_check
        return word_check

    # awalan me-, pe-
    if (word.startswith('me') or word.startswith('pe')) and (len(word) > 2):
        sub_word = word[2:]
        word_check = kamus_word(sub_word)
        if word_check != None:
            word_pref_suff = hapus_derivation_suffiks(word_check)
            word_check = kamus_word(word_pref_suff)
            return word_check
        return word_check
    
    # Direct dictionary check as a last resort
    if word in kamus_clean and word not in AKAR_KATA:
        AKAR_KATA.append(word)
        return None
    
    return word

#%% Metrics calculation
def calculate_metrics(all_words, stemmed_words):
    # Count total words
    total_words = len(all_words)
    
    # Count unique words
    unique_words = len(set(all_words))
    
    # Calculate UI (User Interface)
    UI = unique_words / total_words if total_words > 0 else 0
    
    # Calculate OI (Object Identification)
    recognized_words = len(stemmed_words)
    OI = recognized_words / unique_words if unique_words > 0 else 0
    
    # Calculate MWC (Modified Word Count)
    MWC = unique_words + recognized_words
    
    return {
        'UI': UI,
        'OI': OI,
        'MWC': MWC,
        'total_words': total_words,
        'unique_words': unique_words,
        'recognized_words': recognized_words
    }

#%% MAIN
# Load data
df = pd.read_excel('ArtikelBhsIndo.xlsx')
words = ' '.join(df['Isi'].astype(str).tolist())

# Lowercase and tokenize
words = words.lower()
words = tokenizing(words)

# Split into words
all_words = words.split()
print(f'Jumlah kata awal : {len(all_words)}')

# Apply stopword removal
list_stop_words = []
for w in all_words:
    word = stop_word(w)
    if word is not None:
        list_stop_words.append(word)
print(f'Jumlah kata setelah stop word : {len(list_stop_words)}')

# Direct dictionary check first
for word in list_stop_words:
    if word in kamus_clean:
        if word not in AKAR_KATA:
            AKAR_KATA.append(word)

# Process words not found in dictionary
list_not_in_kamus_words = []
for w in list_stop_words:
    if w not in kamus_clean:
        list_not_in_kamus_words.append(w)

print(f'Jumlah kata setelah kamus : {len(list_not_in_kamus_words)}')
print(f'Akar kata : {len(AKAR_KATA)}')

# Inflectional suffixes removal
list_not_infleksional_suffiks = []
for w in list_not_in_kamus_words:
    word = hapus_infleksional_suffiks(w)
    if word is not None:
        list_not_infleksional_suffiks.append(word)

print(f'Jumlah kata setelah infleksional suffiks : {len(list_not_infleksional_suffiks)}')
print(f'Akar kata : {len(AKAR_KATA)}')

# Derivational suffixes removal
list_not_derivation_suffiks = []
for w in list_not_infleksional_suffiks:
    word = hapus_derivation_suffiks(w)
    if word is not None:
        list_not_derivation_suffiks.append(word)

print(f'Jumlah kata setelah derivation suffiks : {len(list_not_derivation_suffiks)}')
print(f'Akar kata : {len(AKAR_KATA)}')

# Derivational prefixes removal
list_not_in_kamus = []
for w in list_not_derivation_suffiks:
    word = hapus_derivation_prefiks(w)
    if word is not None:
        list_not_in_kamus.append(word)

print(f'Jumlah kata setelah derivation prefiks : {len(list_not_in_kamus)}')
print(f'Akar kata : {len(AKAR_KATA)}')

# Final dictionary check for any missed words
for w in list_not_in_kamus:
    if w in kamus_clean and w not in AKAR_KATA:
        AKAR_KATA.append(w)

print(f'Final akar kata : {len(AKAR_KATA)}')
print(f'Kata yang tak ada di kamus: {len(list_not_in_kamus)}')
print(f"Kata yang tidak ada dikamus: {list_not_in_kamus}")

# Calculate UI, OI, and MWC metrics
metrics = calculate_metrics(all_words, AKAR_KATA)
print(f"UI (User Interface): {metrics['UI']:.4f}")
print(f"OI (Object Identification): {metrics['OI']:.4f}")
print(f"MWC (Modified Word Count): {metrics['MWC']}")
print(f"Total Words: {metrics['total_words']}")
print(f"Unique Words: {metrics['unique_words']}")
print(f"Recognized Words: {metrics['recognized_words']}")
