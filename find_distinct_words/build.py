import os
import pickle
import numpy as np
import gensim
from gensim.models.keyedvectors import KeyedVectors as kv
from find_distinct_words import common_func
from find_distinct_words import tensorly_modified
from collections import Counter


'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code generates ja & ko word2vec models using the filtered k-pop/j-pop files:

--- 'filtered_lyrics/lyrics_ja.p' file
--- 'filtered_lyrics/lyrics_ko.p' file

This code outputs 10 different J-pop/K-pop word2vec models:

--- 'word2vec/w2v_ja_{}.kv' ({}: 0-9)
--- 'word2vec/w2v_ko_{}.kv' ({}: 0-9)

This code outputs 10 different ja, ko, neu's sorted CPD word lists:

--- 'cpd_result/ja_{}.txt' ({}: 0-9)
--- 'cpd_result/ko_{}.txt' ({}: 0-9)
--- 'cpd_result/neu_{}.txt' ({}: 0-9)

This code also outputs the merged(summed) CPD word lists:

--- 'cpd_result/ja.txt'
--- 'cpd_result/ko.txt'
--- 'cpd_result/neu.txt'

'''

# Define new hash function for reproducibility.
# This function is only used in the word2vec() function below.

def new_hash(selected):
    return ord(selected[0])

'''

|++++++++++++|
| word2vec() |
|++++++++++++|

builds two word2vec models, one for j-pop and one for k-pop, and 
saves the model to file.

'''

def word2vec(seed=2018):
    # Create 'word2vec' directory if there isn't any.

    word2vec_dir = "word2vec"
    if not os.path.exists(word2vec_dir):
        os.makedirs(word2vec_dir)

    # Load filtered lyrics data.

    lyrics_ja, lyrics_ko, label = common_func.load_xy()

    # Merge lyrics_ja & lyrics_ko lyrics.

    lyrics = lyrics_ja + lyrics_ko

    # ------------------------------------------------------------------
    # Build J-pop word2vec model.
    # ------------------------------------------------------------------
    # Train word2vec model using both lyrics_ja & lyrics_ko data.

    model_ja = gensim.models.Word2Vec(lyrics, size=5, window=5, min_count=1,
                                      workers=1, seed=seed, hashfxn=new_hash)

    # Retrain word2vec model using only lyrics_ja data to create J-pop word2vec model.

    model_ja.train(lyrics_ja, total_examples=len(lyrics_ja), epochs=50)

    # ------------------------------------------------------------------
    # Build K-pop word2vec model.
    # ------------------------------------------------------------------
    # Train word2vec model using both lyrics_ja & lyrics_ko data.

    model_ko = gensim.models.Word2Vec(lyrics, size=5, window=5, min_count=1,
                                      workers=1, seed=seed, hashfxn=new_hash)

    # Retrain word2vec model using only lyrics_ko data to create K-pop word2vec model.
    model_ko.train(lyrics_ko, total_examples=len(lyrics_ko), epochs=50)

    # Save word2vec model with '.kv' extension ('kv' stands for 'keyvector').

    model_ja.wv.save("word2vec/w2v_ja_{}.kv".format(str(seed)))
    model_ko.wv.save("word2vec/w2v_ko_{}.kv".format(str(seed)))


'''

|++++++++++++++++|
| CPD_wordlist() |
|++++++++++++++++|

builds rank-3 mode-3 CP decomposition tensor using fixed mode-3 values by
importing the 'tensorly_modified' code that modifies the 'tensorly' library.

this modified code performs a fixed mode-3 value CP decomposition.

from the decomposition results, mode-1 vectors are used to sort the index words.

the sorted index words are saved to the 'cpd_result' directory.

'''

def CPD_wordlist(verbose=True, seed=2018):
    # Create 'cpd_result' directory if there isn't any.

    cpd_dir = "cpd_result"
    if not os.path.exists(cpd_dir):
        os.makedirs(cpd_dir)

    kv_ja = kv.load('word2vec/w2v_ja_{}.kv'.format(str(seed)))
    kv_ko = kv.load('word2vec/w2v_ko_{}.kv'.format(str(seed)))
    print("kv_ja.vectors.shape:", kv_ja.vectors.shape)

    X = np.stack((kv_ja.vectors, kv_ko.vectors), axis=2)
    print("stacked X shape:", X.shape)

    w_jako = 0.5
    w_neu = 1.0 - w_jako
    fixed_ja = [w_jako, w_neu, 0.0]  # [0.5, 0.5, 0.0]
    fixed_ko = [0.0, w_neu, w_jako]  # [0.0, 0.5, 0.5]

    country_values = [fixed_ja, fixed_ko]

    # It is important to fix the random_state in order to obtain consistent results.
    # Here, consistent results mean consistent direction of mode-1 word ordering.

    # To ensure convergence, n_iter_max is set at 300.

    decomposed = tensorly_modified.parafac(X, 3, random_state=2018, n_iter_max=300,
                                           mode_three_val=country_values, verbose=verbose)

    # Select mode-1 vectors containing values for the index words and transpose it.

    result = decomposed[0].T

    index_w = kv_ja.index2word

    country = ["ja", "neu", "ko"]

    output = []

    for i in range(3):  # i denotes either 'ja', 'neu', 'ko'.
        val = {}
        for j in range(len(index_w)):
            val[index_w[j]] = result[i][j]
        output.append(val)

        sorted_list = [(k, val[k]) for k in sorted(val, key=val.get, reverse=True)]
        result_str = ""
        word_list = []
        for k, v in sorted_list:
            result_str += "{}\t{}\n".format(k, v)
            word_list.append(k)
        # print(result_str)
        result_file = "{}/{}_{}.txt".format(cpd_dir, country[i], str(seed))
        with open(result_file, 'w') as f:
            f.write(result_str)
    return output



'''

|++++++++++++++++++++++|
| W2V_n_CPD_wordlist() |
|++++++++++++++++++++++|

repeatedly (1) build word2vectors using 'word2vec()' function and 
repeatedly (2) build CPD word list using 'CPD_wordlist()' function which
utilizes fixed mode-3 value CP decomposition.

'''



def W2V_n_CPD_wordlist():
    jako_dict = pickle.load(open("dictionary/ja2ko_dict.p", 'rb'))
    dict_keys = list(jako_dict.values())
    dict_ja = Counter(dict.fromkeys(dict_keys, 0))
    dict_ko = Counter(dict.fromkeys(dict_keys, 0))
    dict_neu = Counter(dict.fromkeys(dict_keys, 0))

    for i in range(10):
        # Build j-pop and k-pop word2vec vectors.

        word2vec(seed=i)

        # Build CPD word list using fixed mode-3 value CP decomposition.

        output = CPD_wordlist(verbose=True, seed=i)

        dict_ja.update(Counter(output[0]))
        dict_neu.update(Counter(output[1]))
        dict_ko.update(Counter(output[2]))

    dict_ja = dict(dict_ja)
    dict_ko = dict(dict_ko)
    dict_neu = dict(dict_neu)

    sorted_list_ja = [(k, dict_ja[k]) for k in sorted(dict_ja, key=dict_ja.get, reverse=True)]
    result_str_ja = ""
    word_list_ja = []
    for k, v in sorted_list_ja:
        result_str_ja += "{}\t{}\n".format(k, v)
        word_list_ja.append(k)
    # print(result_str_ja)
    result_file_ja = "cpd_result/ja.txt"
    with open(result_file_ja, 'w') as f:
        f.write(result_str_ja)

    sorted_list_ko = [(k, dict_ko[k]) for k in sorted(dict_ko, key=dict_ko.get, reverse=True)]
    result_str_ko = ""
    word_list_ko = []
    for k, v in sorted_list_ko:
        result_str_ko += "{}\t{}\n".format(k, v)
        word_list_ko.append(k)
    # print(result_str_ko)
    result_file_ko = "cpd_result/ko.txt"
    with open(result_file_ko, 'w') as f:
        f.write(result_str_ko)

    sorted_list_neu = [(k, dict_neu[k]) for k in sorted(dict_neu, key=dict_neu.get, reverse=True)]
    result_str_neu = ""
    word_list_neu = []
    for k, v in sorted_list_neu:
        result_str_neu += "{}\t{}\n".format(k, v)
        word_list_neu.append(k)
    # print(result_str_neu)
    result_file_neu = "cpd_result/neu.txt"
    with open(result_file_neu, 'w') as f:
        f.write(result_str_neu)

#---------------------------------------
# Builds j-pop and k-pop word2vec vectors and
# # CPD word list using fixed mode-3 value CP decomposition.

#W2V_n_CPD_wordlist()







