import pickle
import numpy as np

'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code reviews the statics of the lyrics data and the coverage of the distinct words.

'''

'''

|+++++++++++++++++++|
| data_statistics() |
|+++++++++++++++++++|

reviews the statics of the lyrics data and the coverage of the distinct words. 

'''


def data_statistics():
    with open("processed/word_list_ko.p", 'rb') as f:
        raw_lyrics_ko = pickle.load(f)
    print("\n# or raw lyrics (KO):", len(raw_lyrics_ko))

    with open("processed/word_list_ja.p", 'rb') as f:
        raw_lyrics_ja = pickle.load(f)
    print("# or raw lyrics (JA):", len(raw_lyrics_ja))

    print("sample of raw lyrics (KO):", raw_lyrics_ko[0][:3])
    print("sample of raw lyrics (JA):", raw_lyrics_ja[0][:3])

    lengths_ko_raw_verbose = [len(i) for i in raw_lyrics_ko]
    lengths_ja_raw_verbose = [len(i) for i in raw_lyrics_ja]

    print("\n# all words *raw* verbose (KO):", sum(lengths_ko_raw_verbose))
    print("# all words *raw* verbose (JA):", sum(lengths_ja_raw_verbose))

    print("avg. word length *raw* verbose (KO):",
          round(float(sum(lengths_ko_raw_verbose)) / len(lengths_ko_raw_verbose), 2))
    print("avg. word length *raw* verbose (JA):",
          round(float(sum(lengths_ja_raw_verbose)) / len(lengths_ja_raw_verbose), 2))

    lengths_ko_raw_uniq = [len(set(i)) for i in raw_lyrics_ko]
    lengths_ja_raw_uniq = [len(set(i)) for i in raw_lyrics_ja]

    print("\n# all words *raw* unique (KO):", sum(lengths_ko_raw_uniq))
    print("# all words *raw* unique (JA):", sum(lengths_ja_raw_uniq))

    print("avg. word length *raw* unique (KO):", round(float(sum(lengths_ko_raw_uniq)) / len(lengths_ko_raw_uniq), 2))
    print("avg. word length *raw* unique (JA):", round(float(sum(lengths_ja_raw_uniq)) / len(lengths_ja_raw_uniq), 2))

    ko_noun = []
    ko_verb = []
    ko_adj = []
    for lyric in raw_lyrics_ko:
        for word in lyric:
            if ":NNG" in word or ":NNP" in word:
                ko_noun.append(word)
            if ":VV" in word:
                ko_verb.append(word)
            if ":VA" in word:
                ko_adj.append(word)

    print("\n# *raw* nouns (KO):", len(ko_noun))
    print("# *raw* verbs (KO):", len(ko_verb))
    print("# *raw* adjectives (KO):", len(ko_adj))

    ja_noun = []
    ja_verb = []
    ja_adj = []
    for lyric in raw_lyrics_ja:
        for word in lyric:
            if ":名詞" in word:
                ja_noun.append(word)
            if ":動詞" in word:
                ja_verb.append(word)
            if ":形容詞" in word:
                ja_adj.append(word)

    print("\n# *raw* nouns (JA):", len(ja_noun))
    print("# *raw* verbs (JA):", len(ja_verb))
    print("# *raw* adjectives (JA):", len(ja_adj))

    print("\n--- raw_v_ko: {}, raw_v_ja: {}, raw_uniq_ko: {}, raw_uniq_ja: {}\n".format(
        len(lengths_ko_raw_verbose), len(lengths_ja_raw_verbose), len(lengths_ko_raw_uniq), len(lengths_ja_raw_uniq)
    ))

    with open("filtered_lyrics/lyrics_ko.p", 'rb') as f:
        lyrics_ko = pickle.load(f)
    print("# of filtered lyrics (KO):", len(lyrics_ko))

    with open("filtered_lyrics/lyrics_ja.p", 'rb') as f:
        lyrics_ja = pickle.load(f)
    print("# of filtered lyrics (JA):", len(lyrics_ja))

    lengths_ko_verbose = [len(i) for i in lyrics_ko]
    lengths_ja_verbose = [len(i) for i in lyrics_ja]
    print("sample of filtered lyrics (KO):", lyrics_ko[0][:3])
    print("sample of filtered lyrics (JA):", lyrics_ja[0][:3])

    print("\n# all words *filtered* verbose (KO):", sum(lengths_ko_verbose))
    print("# all words *filtered* verbose (JA):", sum(lengths_ja_verbose))

    print("avg. word length *filtered* verbose (KO):",
          round(float(sum(lengths_ko_verbose)) / len(lengths_ko_verbose), 2))
    print("avg. word length *filtered* verbose (JA):",
          round(float(sum(lengths_ja_verbose)) / len(lengths_ja_verbose), 2))

    lengths_ko_uniq = [len(set(i)) for i in lyrics_ko]
    lengths_ja_uniq = [len(set(i)) for i in lyrics_ja]

    print("\n# all words *filtered* unique (KO):", sum(lengths_ko_uniq))
    print("# all words *filtered* unique (JA):", sum(lengths_ja_uniq))

    print("avg. word length *filtered* uniq (KO):", round(float(sum(lengths_ko_uniq)) / len(lengths_ko_uniq), 2))
    print("avg. word length *filtered* uniq (JA):", round(float(sum(lengths_ja_uniq)) / len(lengths_ja_uniq), 2))

    ko_noun = []
    ko_verb = []
    ko_adj = []
    for lyric in lyrics_ko:
        for word in lyric:
            if (":NNG" in word) or (":NNP" in word):
                ko_noun.append(word)
            if ":VV" in word:
                ko_verb.append(word)
            if ":VA" in word:
                ko_adj.append(word)

    print("\n# *filtered* nouns (KO):", len(ko_noun))
    print("# *filtered* verbs (KO):", len(ko_verb))
    print("# *filtered* adjectives (KO):", len(ko_adj))

    # Note that the filtered_lyrics_ja contain Japanese --> Korean mapping of J-pop lyrics.
    ja_noun = []
    ja_verb = []
    ja_adj = []
    for lyric in lyrics_ja:
        for word in lyric:
            if (":NNG" in word) or (":NNP" in word):
                ja_noun.append(word)
            if ":VV" in word:
                ja_verb.append(word)
            if ":VA" in word:
                ja_adj.append(word)

    print("\n# *filtered* nouns (JA):", len(ja_noun))
    print("# *filtered* verbs (JA):", len(ja_verb))
    print("# *filtered* adjectives (JA):", len(ja_adj))

    print("\n--- flt_v_ko: {}, flt_v_ja: {}, flt_uniq_ko: {}, flt_uniq_ja: {}\n".format(
        len(lengths_ko_verbose), len(lengths_ja_verbose), len(lengths_ko_uniq), len(lengths_ja_uniq)
    ))

    print("\n--- COVERAGE IN % ---\n")
    print("filtered_words/all_words_raw (%) (KO):",
          round(float(sum(lengths_ko_verbose)) / sum(lengths_ko_raw_verbose), 5))
    print("filtered_words/all_words_raw (%) (JA):",
          round(float(sum(lengths_ja_verbose)) / sum(lengths_ja_raw_verbose), 5))

    print("filtered_words_uniq/all_words_raw_uniq (%) (KO):",
          round(float(sum(lengths_ko_uniq)) / sum(lengths_ko_raw_uniq), 5))
    print("filtered_words_uniq/all_words_raw_uniq (%) (JA):",
          round(float(sum(lengths_ja_uniq)) / sum(lengths_ja_raw_uniq), 5))

    print("\n--- COVERAGE OF DISTINCT WORDS ---")

    # Coverage of the distinct words.

    with open("result/distinct_words.p", 'rb') as f:
        distinct = pickle.load(f)

    print("\nSize of distinct words (KO):", len(distinct))

    coverage_distinct_ko = []
    for lyric in lyrics_ko:
        counter = 0
        init_length = len(lyric)
        for w in lyric:
            if w in distinct:
                counter += 1
        coverage_distinct_ko.append(float(counter) / init_length)

    print("Coverage of distinct words in filtered lyrics K-pop:", round(np.mean(np.array(coverage_distinct_ko)), 5))

    coverage_distinct_ja = []
    for lyric in lyrics_ja:
        counter = 0
        init_length = len(lyric)
        for w in lyric:
            if w in distinct:
                counter += 1
        coverage_distinct_ja.append(float(counter) / init_length)

    print("Coverage of distinct words in filtered lyrics J-pop:", round(np.mean(np.array(coverage_distinct_ja)), 5))

    print("\n------------------------------------\n")

    with open("dictionary/ja2ko_dict.p", 'rb') as f:
        jako_dict = pickle.load(f)

    ind_w_dict_ja = []
    ind_w_dict_ko = []

    for k, v in jako_dict.items():
        if '|' in k:
            ind_w_dict_ja += k.split('|')
        else:
            ind_w_dict_ja.append(k)

        if '|' in v:
            ind_w_dict_ko += v.split('|')
        else:
            ind_w_dict_ko.append(v)


    print("Individual ko_words in dict:", len(ind_w_dict_ko))
    print("Individual ja_words in dict:", len(ind_w_dict_ja))


# Presents overview statistics of the lyrics data.

#data_statistics()


'''
/usr/bin/python3 /home/hcilab/Documents/OSS/playnview_distinctwordfinder/find_distinct_words/review.py

# or raw lyrics (KO): 1000
# or raw lyrics (JA): 1142
sample of raw lyrics (KO): ['쳐다보:VV', '예쁘:VA', '그렇:VA']
sample of raw lyrics (JA): ['ゆれる:動詞', '光:名詞', 'ひとつ:名詞']

# all words *raw* verbose (KO): 77092
# all words *raw* verbose (JA): 125205
avg. word length *raw* verbose (KO): 77.09
avg. word length *raw* verbose (JA): 109.64

# all words *raw* unique (KO): 43051
# all words *raw* unique (JA): 82319
avg. word length *raw* unique (KO): 43.05
avg. word length *raw* unique (JA): 72.08

# *raw* nouns (KO): 51161
# *raw* verbs (KO): 18413
# *raw* adjectives (KO): 7518

# *raw* nouns (JA): 77859
# *raw* verbs (JA): 41353
# *raw* adjectives (JA): 5993

--- raw_v_ko: 1000, raw_v_ja: 1142, raw_uniq_ko: 1000, raw_uniq_ja: 1142

# of filtered lyrics (KO): 987
# of filtered lyrics (JA): 1134
sample of filtered lyrics (KO): ['보:VV|쳐다보:VV|바라보:VV|올려다보:VV', '귀엽:VA|이쁘:VA|예쁘:VA', '보:VV|쳐다보:VV|바라보:VV|올려다보:VV']
sample of filtered lyrics (JA): ['빛:NNG', '하나:NNG', '아파하:VV']

# all words *filtered* verbose (KO): 59673
# all words *filtered* verbose (JA): 65301
avg. word length *filtered* verbose (KO): 60.46
avg. word length *filtered* verbose (JA): 57.58

# all words *filtered* unique (KO): 30935
# all words *filtered* unique (JA): 41595
avg. word length *filtered* uniq (KO): 31.34
avg. word length *filtered* uniq (JA): 36.68

# *filtered* nouns (KO): 39316
# *filtered* verbs (KO): 13771
# *filtered* adjectives (KO): 6690

# *filtered* nouns (JA): 35591
# *filtered* verbs (JA): 25437
# *filtered* adjectives (JA): 4564

--- flt_v_ko: 987, flt_v_ja: 1134, flt_uniq_ko: 987, flt_uniq_ja: 1134


--- COVERAGE IN % ---

filtered_words/all_words_raw (%) (KO): 0.77405
filtered_words/all_words_raw (%) (JA): 0.52155
filtered_words_uniq/all_words_raw_uniq (%) (KO): 0.71857
filtered_words_uniq/all_words_raw_uniq (%) (JA): 0.50529

--- COVERAGE OF DISTINCT WORDS ---

Size of distinct words (KO): 545
Coverage of distinct words in filtered lyrics K-pop: 0.57954
Coverage of distinct words in filtered lyrics J-pop: 0.61315

------------------------------------

Individual ko_words in dict: 1158
Individual ja_words in dict: 1338

Process finished with exit code 0

'''