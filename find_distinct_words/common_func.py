import os
import pickle
import numpy as np
import pandas as pd

'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code includes some common functions that are repeatedly used:

--- load_xy() : loads filtered lyrics data.
--- load_word_list(weight) : loads CP decomposition J-pop, K-pop, & Neutral 
                             word lists which are saved under the 'cpd_result' directory.
--- get_avg(mean_list) : calculates the mean average clustering performance.
--- save_distinct_words(distinct_wordlist, label) : saves the J-pop/K-pop distinct word lists.

'''


'''

|+++++++++++|
| load_xy() |
|+++++++++++|

load filtered J-pop & K-pop lyrics data.

'''

def load_xy():
    with open("filtered_lyrics/lyrics_ja.p", 'rb') as f:
        lyrics_ja = pickle.load(f)
    print("lyrics ja:", len(lyrics_ja))

    with open("filtered_lyrics/lyrics_ko.p", 'rb') as f:
        lyrics_ko = pickle.load(f)
    print("lyrics ko:", len(lyrics_ko))

    label_ja = [1] * len(lyrics_ja)
    label_ko = [0] * len(lyrics_ko)
    label = label_ja + label_ko

    return lyrics_ja, lyrics_ko, label


'''

|++++++++++++++++++++++++|
| load_word_list(weight) |
|++++++++++++++++++++++++|

loads CP decomposition (CPD) applied word lists. (J-pop, K-pop, Neutral)

'''

def load_word_list():
    df_ja = pd.read_csv("cpd_result/ja.txt", header=None, delimiter='\t')
    word_list_ja = list(df_ja[0].values)

    df_ko = pd.read_csv("cpd_result/ko.txt", header=None, delimiter='\t')
    word_list_ko = list(df_ko[0].values)

    df_neu = pd.read_csv("cpd_result/neu.txt", header=None, delimiter='\t')
    word_list_neu = list(df_neu[0].values)

    return word_list_ja, word_list_ko, word_list_neu

'''

|++++++++++++++++++++|
| get_avg(mean_list) |
|++++++++++++++++++++|

calculates the average performance of the multi-trial experiments.

'''

def get_avg(mean_list):
    row_avg = np.mean(np.array(mean_list), axis=1)
    for i in range(len(row_avg)):
        mean_list[i].append(row_avg[i])
    column_avg = np.mean(np.array(mean_list), axis=0)
    mean_list.append(list(column_avg))
    func = lambda x: round(x, 5)
    mean_list = [list(map(func, i)) for i in mean_list]
    return mean_list


'''

|++++++++++++++++++++++++++++++++++++++++++++++++++|
| save_distinct_words_ko(distinct_wordlist, label) |
|++++++++++++++++++++++++++++++++++++++++++++++++++|

saves distinct K-pop/J-pop/Neutral CPD words (in Korean) to the 'result_ko' folder.

'''

def save_distinct_words_ko(distinct_wordlist, label):
    # Create 'result' directory if there isn't any.

    result_dir = "result_ko"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    print("\n----------------------------------------")
    print("     DISTINCT {} WORDS : KO    ".format(label.upper()))
    print("----------------------------------------")

    freq_ko = pd.read_csv("processed/uniq_word_ko.txt", header=None, delimiter='\t')

    with open("dictionary/ja2ko_dict.p", 'rb') as f:
        jako_dict = pickle.load(f)

    matched_ko = []
    for key_ja, val_ko in jako_dict.items():
        if val_ko in distinct_wordlist:
            matched_ko.append(val_ko)
    print("matched_{}:".format(label), len(matched_ko))

    split_ko = []
    for w in matched_ko:
        if '|' in w:
            split_ko += w.split('|')
        else:
            split_ko.append(w)
    print("split_{}:".format(label), len(split_ko))

    selected_ko = freq_ko[freq_ko[0].isin(split_ko)]
    sorted_ko = selected_ko.sort_values([1], ascending=[False])

    sorted_ko.to_csv("result_ko/distinct_{}.csv".format(label), header=None, index=None)

    ko_nng = sorted_ko[sorted_ko[0].str.contains(":NNG")]
    ko_nng.to_csv("result_ko/distinct_{}_NNG.csv".format(label), header=None, index=None)

    ko_nnp = sorted_ko[sorted_ko[0].str.contains(":NNP")]
    ko_nnp.to_csv("result_ko/distinct_{}_NNP.csv".format(label), header=None, index=None)

    ko_va = sorted_ko[sorted_ko[0].str.contains(":VA")]
    ko_va.to_csv("result_ko/distinct_{}_VA.csv".format(label), header=None, index=None)

    ko_vv = sorted_ko[sorted_ko[0].str.contains(":VV")]
    ko_vv.to_csv("result_ko/distinct_{}_VV.csv".format(label), header=None, index=None)


'''

|++++++++++++++++++++++++++++++++++++++++++++++++++|
| save_distinct_words_ja(distinct_wordlist, label) |
|++++++++++++++++++++++++++++++++++++++++++++++++++|

saves distinct K-pop/J-pop/Neutral CPD words (in Japanese) to the 'result_ja' folder.

'''

def save_distinct_words_ja(distinct_wordlist, label):
    # Create 'result' directory if there isn't any.

    result_dir = "result_ja"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    print("\n----------------------------------------")
    print("     DISTINCT {} WORDS : JA    ".format(label.upper()))
    print("----------------------------------------")

    freq_ja = pd.read_csv("processed/uniq_word_ja.txt", header=None, delimiter='\t')

    with open("dictionary/ja2ko_dict.p", 'rb') as f:
        jako_dict = pickle.load(f)

    matched_ja = []
    for key_ja, val_ko in jako_dict.items():
        if val_ko in distinct_wordlist:
            matched_ja.append(key_ja)
    print("matched_{}:".format(label), len(matched_ja))

    split_ja = []
    for w in matched_ja:
        if '|' in w:
            split_ja += w.split('|')
        else:
            split_ja.append(w)
    print("split_{}:".format(label), len(split_ja))

    selected_ja = freq_ja[freq_ja[0].isin(split_ja)]
    sorted_ja = selected_ja.sort_values([1], ascending=[False])

    sorted_ja.to_csv("result_ja/distinct_{}.csv".format(label), header=None, index=None)

    ja_nng = sorted_ja[sorted_ja[0].str.contains(":名詞")]
    ja_nng.to_csv("result_ja/distinct_{}_noun.csv".format(label), header=None, index=None)

    ja_va = sorted_ja[sorted_ja[0].str.contains(":形容詞")]
    ja_va.to_csv("result_ja/distinct_{}_adjective.csv".format(label), header=None, index=None)

    ja_vv = sorted_ja[sorted_ja[0].str.contains(":動詞")]
    ja_vv.to_csv("result_ja/distinct_{}_verb.csv".format(label), header=None, index=None)
