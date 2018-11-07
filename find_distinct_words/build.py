import os
import numpy as np
import gensim
from gensim.models.keyedvectors import KeyedVectors as kv
from find_distinct_words import common_func
from find_distinct_words import tensorly_modified


'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code generates ja & ko word2vec models using the filtered k-pop/j-pop files:

--- 'filtered_lyrics/lyrics_ja.p' file
--- 'filtered_lyrics/lyrics_ko.p' file

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

def word2vec():
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
                                      workers=1, seed=2019, hashfxn=new_hash)

    # Retrain word2vec model using only lyrics_ja data to create J-pop word2vec model.

    model_ja.train(lyrics_ja, total_examples=len(lyrics_ja), epochs=50)

    # ------------------------------------------------------------------
    # Build K-pop word2vec model.
    # ------------------------------------------------------------------
    # Train word2vec model using both lyrics_ja & lyrics_ko data.

    model_ko = gensim.models.Word2Vec(lyrics, size=5, window=5, min_count=1,
                                      workers=1, seed=2018, hashfxn=new_hash)

    # Retrain word2vec model using only lyrics_ko data to create K-pop word2vec model.
    model_ko.train(lyrics_ko, total_examples=len(lyrics_ko), epochs=50)

    # Save word2vec model with '.kv' extension ('kv' stands for 'keyvector').

    model_ja.wv.save("word2vec/w2v_ja.kv")
    model_ko.wv.save("word2vec/w2v_ko.kv")


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

def CPD_wordlist():
    # Create 'cpd_result' directory if there isn't any.

    cpd_dir = "cpd_result"
    if not os.path.exists(cpd_dir):
        os.makedirs(cpd_dir)

    kv_ja = kv.load('word2vec/w2v_ja.kv')
    kv_ko = kv.load('word2vec/w2v_ko.kv')
    print("kv_ja.vectors.shape:", kv_ja.vectors.shape)

    X = np.stack((kv_ja.vectors, kv_ko.vectors), axis=2)
    print("stacked X shape:", X.shape)

    w_jako = 0.5
    w_neu = 1.0 - w_jako
    fixed_ja = [w_jako, w_neu, 0.0]  # e.g., [0.1, 0.9, 0.0]
    fixed_ko = [0.0, w_neu, w_jako]  # e.g., [0.0, 0.9, 0.1]

    country_values = [fixed_ja, fixed_ko]
    decomposed = tensorly_modified.parafac(X, 3, random_state=2018, mode_three_val=country_values)

    # Select mode-1 vectors containing values for the index words and transpose it.

    result = decomposed[0].T

    index_w = kv_ja.index2word

    country = ["ja", "neu", "ko"]

    for i in range(3):  # i denotes either 'ja', 'neu', 'ko'.
        val = {}
        for j in range(len(index_w)):
            val[index_w[j]] = result[i][j]
        sorted_list = [(k, val[k]) for k in sorted(val, key=val.get, reverse=True)]
        result_str = ""
        word_list = []
        for k, v in sorted_list:
            result_str += "{}\t{}\n".format(k, v)
            word_list.append(k)
        # print(result_str)
        result_file = "{}/{}.txt".format(cpd_dir, country[i])
        with open(result_file, 'w') as f:
            f.write(result_str)



# Execute the below functions in a sequential manner.

#---------------------------------------
# Build j-pop and k-pop word2vec vectors.

word2vec()

#---------------------------------------
# Build CPD word list using fixed mode-3 value CP decomposition.

CPD_wordlist()
