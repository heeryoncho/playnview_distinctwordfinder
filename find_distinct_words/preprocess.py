import os
import pandas as pd
import MeCab
from konlpy.tag import Mecab
import re
import pickle
from collections import Counter

'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code performs the following preprocessing of the lyrics data:

1. Tokenization (extracts nouns, verbs, and adjectives).

2. Filtering of the tokenized J-pop/K-pop lyrics word and obtaining 
   Japanese index words using the J-pop/K-pop lyrics word alignment dictionary.
   
   <sample entry of the alignment dictionary>
   夢:名詞|ゆめいっぱい:名詞          꿈:NNG
   
   J-pop lyrics word '夢:名詞' is replaced with '夢:名詞|ゆめいっぱい:名詞' through filtering.
   K-pop lyrics word '꿈:NNG' is replaced with '夢:名詞|ゆめいっぱい:名詞' through filtering.

Hence, through the filtering process, K-pop lyrics words are also converted to 
Japanese dictionary index words.

The J-pop/K-pop lyrics word alignment dictionary is manually created by
two language professionals, and has 1,007 index words.

A function that checks the content of the dictionary, and 
saves the dictionary to more accessible pickle file is also provided.
See 'check_dictionary()' function. 

'''


'''

|++++++++++++++++++++++++++|
| tokenize_ja(lyrics_file) |
|++++++++++++++++++++++++++|

tokenizes J-pop lyrics data by extracting nouns, verbs and adjectives.

'''

def tokenize_ja(lyrics_file_ja):
    print("\n-------- J-POP LYRICS --------")

    # lyrics_file_ja = ../crawl_data/lyrics_jp/jp_lyrics_verbose.csv
    df = pd.read_csv(lyrics_file_ja)
    print(df.shape, "# as_is_ja")
    df = df.dropna()
    print(df.shape, "# dropna()")
    df = df.drop_duplicates()
    print(df.shape, "# drop_duplicates()")

    data = list(df['Lyrics'].values)
    print("num. of lyrics_ja:", len(data))

    # Load Japanese stopwords.

    with open('stopwords/stopwords-ja.txt', 'r') as f:
        stopwords = f.read()
        stopwords = stopwords.split("\n")

    # Load Japanese morphological analyzer.

    NEOLOGD = "-Ochasen -d /usr/lib/mecab/dic/mecab-ipadic-neologd"
    m = MeCab.Tagger(NEOLOGD)

    lines = []
    for lyric in data:
        # Remove English words.
        lyric = re.sub('[a-zA-z]', '', lyric)
        morph = []
        m.parse('')
        lex = m.parseToNode(re.sub('\u3000', ' ', lyric))
        while lex:
            # Insert tokens to dictionary
            tmp = {}
            tmp['surface'] = lex.surface
            tmp['base'] = lex.feature.split(',')[-3]  # base
            tmp['pos'] = lex.feature.split(',')[0]  # pos
            tmp['pos1'] = lex.feature.split(',')[1]  # pos1
            # Beginning and ending of a sentence are no included.
            if 'BOS/EOS' not in tmp['pos']:
                morph.append(tmp)
            lex = lex.next
        lines.append(morph)

    # If 'base' word exists, use 'base' word; otherwise use 'surface' word.
    word_list = []
    for line in lines:
        tmp = []
        for morph in line:
            if (morph['pos'] == '名詞') | (morph['pos'] == '動詞') | (morph['pos'] == '形容詞'):
                if (not morph['base'] == '*') & (morph['base'] not in stopwords):
                    tmp.append("{}:{}".format(morph['base'], morph['pos']))
                elif (morph['surface'] not in stopwords):
                    tmp.append("{}:{}".format(morph['surface'], morph['pos']))
        word_list.append(tmp)

    # Create 'processed' directory if there isn't any.

    processed_dir = "processed"
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    # Save tokenized lyrics, which contains nouns, verbs, and adjectives, to file.

    with open("processed/word_list_ja.p", 'wb') as f:
        pickle.dump(word_list, f)

    flat_list = [item for sublist in word_list for item in sublist]
    print("total_ja_words:", len(flat_list))

    counts = Counter(flat_list)
    print("uniq_words_ja:", len(counts))

    # Save unique word list with frequency to file.

    with open("processed/uniq_word_ja.txt", 'w') as f:
        for k, v in counts.most_common():
            f.write("{}\t{}\n".format(k, v))

'''

|++++++++++++++++++++++++++|
| tokenize_ko(lyrics_file) |
|++++++++++++++++++++++++++|

tokenizes K-pop lyrics data by extracting 
nouns (common noun & proper noun), verbs and adjectives.

'''

def tokenize_ko(lyrics_file_ko):
    print("\n-------- K-POP LYRICS --------")

    # lyrics_file_ko = "../crawl_data/lyrics_kr/kr_lyrics_verbose.csv"
    df = pd.read_csv(lyrics_file_ko)
    print(df.shape, "# as_is_ko")
    df = df.dropna()
    print(df.shape, "# dropna()")
    df = df.drop_duplicates()
    print(df.shape, "# drop_duplicates()")

    data = list(df['Lyrics'].values)
    print("ko num of lyrics:", len(data))

    # Load Korean stopwords.

    stopwords = ["하:VV", "있:VV", "되:VV", "있:VA", "이러:VV"]

    # Load Korean morphological analyzer.

    mecab = Mecab()

    morphs = []
    for lyric in data:
        lyric = re.sub('[a-zA-z]', '', lyric)
        parsed = mecab.pos(lyric)
        tmp = []
        for w, pos in parsed:
            # We look for four parts of speech
            # See below URL for POS tags (Mecab-ko)
            # *** KoNLPy Korean POS Tag Comparison Chart ***
            # https://docs.google.com/spreadsheets/d/1OGAjUvalBuX-oZvZ_-9tEfYD2gQe7hTGsgUpiiBSXI8/edit#gid=0
            if (pos == 'NNG') | (pos == 'NNP') | (pos == 'VV') | (pos == 'VA'):
                wpos = "{}:{}".format(w, pos)
                if wpos not in stopwords:
                    tmp.append(wpos)
        morphs.append(tmp)

    # Create 'processed' directory if there isn't any.

    processed_dir = "processed"
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    with open("processed/word_list_ko.p", 'wb') as f:
        pickle.dump(morphs, f)

    flat_list = [item for sublist in morphs for item in sublist]
    print("total_ko_words:", len(flat_list))

    counts = Counter(flat_list)
    print("uniq_words_ko:", len(counts))

    with open("processed/uniq_word_ko.txt", 'w') as f:
        for k, v in counts.most_common():
            f.write("{}\t{}\n".format(k, v))


'''

|++++++++++++++++++++|
| check_dictionary() |
|++++++++++++++++++++|

checks the content of the manually created J-pop/K-pop lyrics word alignment dictionary.

'''

def check_dictionary():
    print("\n-------- J-POP/K-POP LYRICS WORD ALIGNMENT DICTIONARY --------")
    df_dict = pd.read_csv('dictionary/ja2ko_aligned_dict_final.csv', delimiter='\t')
    print(df_dict.head(3))
    print("\njako_dict shape:", df_dict.shape)

    # Counts individual dictionary word (ungrouped), i.e., indiv_dword_country.

    indiv_dword_ko = []
    indiv_dword_ja = []
    for idx, row in df_dict.iterrows():
        ja_w = row[0]
        ko_w = row[1]
        if (':NNG' in ko_w) | (':NNP' in ko_w) | (':VV' in ko_w) | (':VA' in ko_w):
            if '|' in ko_w:
                indiv_dword_ko += ko_w.split("|")
            else:
                indiv_dword_ko.append(ko_w)
            if '|' in ja_w:
                indiv_dword_ja += ja_w.split("|")
            else:
                indiv_dword_ja.append(ja_w)
        else:
            print("other_POS:", ko_w)

    print("\n# of indiv. ko_words:", len(indiv_dword_ko), "check uniqueness:", len(set(indiv_dword_ko)))
    print("# of indiv. ja_words:", len(indiv_dword_ja), "check uniqueness:", len(set(indiv_dword_ja)))

    uniq_word_ko = pd.read_csv("processed/uniq_word_ko.txt", delimiter='\t', header=None)
    uniq_word_ja = pd.read_csv("processed/uniq_word_ja.txt", delimiter='\t', header=None)

    uw_ko = uniq_word_ko[0].values
    uw_ja = uniq_word_ja[0].values

    diff_ko = set(indiv_dword_ko) - set(uw_ko)
    print("\ndiff_ko:", len(diff_ko), diff_ko)

    diff_ja = set(indiv_dword_ja) - set(uw_ja)
    print("diff_ja:", len(diff_ja), diff_ja)

    if '' in indiv_dword_ko:
        print("empty string!")

    for ind, elem in enumerate(indiv_dword_ko):
        if elem == '':
            print(ind)
            break

    # Create ja-ko dictionary by rearranging J-pop/K-pop alignment dictionary.
    # Ja-ko dictionary is used to filter the J-pop lyrics (so that Korean
    # word list is obtained also for J-pop lyrics.)

    jako_dict = pd.Series(df_dict.word_ko.values, index=df_dict.word_ja).to_dict()

    # Save ja-ko dictionary.

    with open("dictionary/ja2ko_dict.p", 'wb') as f:
       pickle.dump(jako_dict, f)



'''

|+++++++++++++++++|
| filter_lyrics() |
|+++++++++++++++++|

filters the lyrics data using the following 3 files:

1. 'dictionary/ko2ja_dict.p'
2. 'processed/uniq_word_ja.txt' file
3. 'processed/uniq_word_ko.txt' file

the output files are:

1. "filtered_lyrics/lyrics_ja.p"
2. "filtered_lyrics/lyrics_ko.p"

the filtered lyrics data contain index words listed in the 
J-pop/K-pop lyrics word alignment dictionary 
('dictionary/ja2ko_aligned_dict_final.csv' or 'dictionary/ko2ja_dict.p')

'''

def filter_lyrics():
    print("\n-------- FILTERED LYRICS --------")

    # Create 'filtered_lyrics' directory if it does not exist.

    filtered_lyrics_dir = "filtered_lyrics"
    if not os.path.exists(filtered_lyrics_dir):
        os.makedirs(filtered_lyrics_dir)

    # Load manually created lyrics-specific Japanese-Korean dictionary.

    jako_dict = pickle.load(open("dictionary/ja2ko_dict.p", 'rb'))

    # Split grouped Korean words.

    ko_list = list(jako_dict.values())
    ko_hash = {}
    for ko in ko_list:
        if "|" in ko:
            splitted_ko = ko.split("|")
            for each in splitted_ko:
                ko_hash[each] = ko
        else:
            ko_hash[ko] = ko

    # Read K-pop lyrics data.

    with open("processed/word_list_ko.p", 'rb') as f:
        ko_lyrics = pickle.load(f)

    ko_filtered = []
    for each_lyric in ko_lyrics:
        tmp = []
        for w in each_lyric:
            if w in ko_hash:
                tmp.append(ko_hash[w])
        if tmp != []:
            ko_filtered.append(tmp)
    print("\n# of matching k-pop lyrics texts:", len(ko_filtered))

    flat_list_ko = [item for sublist in ko_filtered for item in sublist]
    print("filtered k-pop unique word indices:", len(set(flat_list_ko)))

    # Save filtered_ko lyrics:

    with open("filtered_lyrics/lyrics_ko.p", 'wb') as f:
        pickle.dump(ko_filtered, f)

    # Read J-pop lyrics data.

    with open("processed/word_list_ja.p", 'rb') as f:
        ja_lyrics = pickle.load(f)


    ja_list = list(jako_dict.keys())
    ja_hash = {}
    for ja in ja_list:
        if "|" in ja:
            splitted_ja = ja.split("|")
            for each in splitted_ja:
                ja_hash[each] = ja
        else:
            ja_hash[ja] = ja

    ja_filtered = []
    for each_lyric in ja_lyrics:
        tmp = []
        for w in each_lyric:
            if w in ja_hash:
                tmp.append(jako_dict[ja_hash[w]])
        if tmp != []:
            ja_filtered.append(tmp)
    print("\n# of matching ja lyrics texts:", len(ja_filtered))

    flat_list_ja = [item for sublist in ja_filtered for item in sublist]
    print("filtered j-pop unique word indices:", len(set(flat_list_ja)))

    # Save filtered_ja lyrics:
    # *** Note that Japanese lyrics words are mapped to Korean word tokes. ***
    with open("filtered_lyrics/lyrics_ja.p", 'wb') as f:
        pickle.dump(ja_filtered, f)

    # Merge filtered_ja & filtered_ko lyrics
    filtered = ja_filtered + ko_filtered
    print("\ntotal num of lyrics (ja+ko):", len(filtered))


# Execute the below functions in a sequential manner.

#---------------------------------------
# Tokenize j-pop lyrics data and extract nouns, verbs, and adjectives.

#tokenize_ja("../crawl_data/lyrics_jp/jp_lyrics_verbose.csv")

#---------------------------------------
# Tokenize k-pop lyrics data and extract nouns (common nouns and proper nouns), verbs, and adjectives.

#tokenize_ko("../crawl_data/lyrics_kr/kr_lyrics_verbose.csv")

#---------------------------------------
# Check the content of the manually created J-pop/K-pop lyrics word alignment dictionary,
# and convert the dictionary content into a python dictionary with
# k-pop index words as key and j-pop dictionary as values.
# Save the converted python dictionary (ko2ja_dict) using pickle.

#check_dictionary()

#---------------------------------------
# Filter k-pop & j-pop lyrics data using the alignment dictionary and
# save the result to 'filtered_lyrics' directory.
# The filtered data are used hereinafter.

#filter_lyrics()


'''

/usr/bin/python3 /home/hcilab/Documents/OSS/playnview/find_distinct_words/preprocess.py

-------- J-POP LYRICS --------
(1142, 6) # as_is_ja
(1142, 6) # dropna()
(1142, 6) # drop_duplicates()
num. of lyrics_ja: 1142
total_ja_words: 125205
uniq_words_ja: 13086

-------- K-POP LYRICS --------
(1000, 6) # as_is_ko
(1000, 6) # dropna()
(1000, 6) # drop_duplicates()
ko num of lyrics: 1000
total_ko_words: 77092
uniq_words_ko: 5797

-------- J-POP/K-POP LYRICS WORD ALIGNMENT DICTIONARY --------
                    word_ja        word_ko
0                今:名詞|いま:名詞  지금:NNG|이제:NNG
1            夢:名詞|ゆめいっぱい:名詞          꿈:NNG
2  愛:名詞|恋:名詞|愛してる:名詞|恋と愛:名詞         사랑:NNG

jako_dict shape: (1007, 2)

# of indiv. ko_words: 1158 check uniqueness: 1158
# of indiv. ja_words: 1338 check uniqueness: 1338

diff_ko: 0 set()
diff_ja: 0 set()

-------- FILTERED LYRICS --------

# of matching ja lyrics texts: 1134
filtered ja unique word indices: 1007

# of matching ko lyrics texts: 987
filtered ko unique word indices: 1007

total num of lyrics (ja+ko): 2121

Process finished with exit code 0

'''
