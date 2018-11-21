import os
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from find_distinct_words import common_func
from pylab import *


'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code calculates the clustering performance of J-pop and K-pop CPD words. 
This code tests 4 cases where J-pop & K-pop CPD words are selected from:

1. top-N J-pop & top-N K-pop
2. top-N J-pop & bottom-N K-pop
3. bottom-N J-pop & top-N K-pop
4. bottom-N J-pop & bottom-N K-pop

CPD words.

'''



'''

|++++++++++++|
| baseline() |
|++++++++++++|

calculates the average clustering performance of the multi-trial experiments
using all filtered words (i.e., 1,007 index words).

'''

def baseline():
    # Create 'table' directory if there isn't any.

    table_dir = "table"
    if not os.path.exists(table_dir):
        os.makedirs(table_dir)

    # Load filtered lyrics data and y_label.

    lyrics_ja, lyrics_ko, label = common_func.load_xy()

    lyrics_all = lyrics_ja + lyrics_ko

    tfidf = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=lambda x: x)
    vect = tfidf.fit_transform(lyrics_all)
    print("# tfidf vect shape:", vect.shape)
    print("# tfidf vect features:", tfidf.get_feature_names()[:3])

    num_clusters = 2

    # Conduct clustering experiments using 5 different seeds.

    ari_list = []

    # To save execution time, one trial experiment is conducted instead of five.
    # for i in range(5):
    for i in range(1):
        km = KMeans(n_clusters=num_clusters, random_state=i)
        y_predict = km.fit_predict(vect)

        ari = adjusted_rand_score(y_predict, label)
        print("trial_{}: ari={:.5f}".format(i+1, ari))

        ari_list.append(ari)

    mean_ari = float(sum(ari_list)) / max(len(ari_list), 1)

    print("\n--- BASELINE TFIDF ---\n")
    print("ARI: {:.5f}".format(round(mean_ari, 5)))

    f_tfidf = "{}/tfidf.txt".format(table_dir)
    with open(f_tfidf, "w") as f:
        f.write(str(mean_ari))


'''

|++++++++++++++++|
| top_x_bottom() |
|++++++++++++++++|

calculates the average clustering performance of the multi-trial experiments
using various top_n/bottom_n X bottom_n/top_n, j-pop and k-pop CPD words.

a 2 X 2 = 4 cases of clustering performances are investigated.

'''

def top_x_bottom():
    # Create 'table' directory if there isn't any.

    table_dir = "table"
    if not os.path.exists(table_dir):
        os.makedirs(table_dir)

    # Load data and y_label.

    lyrics_ja, lyrics_ko, label = common_func.load_xy()

    # 4 cases are tested: top-top, top-bottom, bottom-top, bottom-bottom (J-pop vs. K-pop).

    cases = ["tt", "tb", "bt", "bb"]

    for case in cases:
        if case is "tt":
            print("\n\n=========================================================")
            print("                     ja_TOP X ko_TOP                     ")
            print("=========================================================")

        if case is "tb":
            print("\n\n=========================================================")
            print("                    ja_TOP X ko_BOTTOM                   ")
            print("=========================================================")

        if case is "bt":
            print("\n\n=========================================================")
            print("                    ja_BOTTOM X ko_TOP                   ")
            print("=========================================================")

        if case is "bb":
            print("\n\n=========================================================")
            print("                ja_BOTTOM X ko_BOTTOM                    ")
            print("=========================================================")

        # Container for the Adjusted Rand Index (ARI) output using various mode-3 value CPD results, and
        # number of j-pop + k-pop index words used in the clustering.

        result_ari = []
        result_n_w = []

        #tmp_ari = []
        #tmp_n_w = []

        # Load CPD word list.

        ja, ko, neu = common_func.load_word_list()

        # Reverse the list; this is done to retrieve bottom-n words.

        rev_ja = list(reversed(ja))
        rev_ko = list(reversed(ko))

        for top_n in range(50, 1050, 50):
            # *** Top-N vs. Top-N *** -------------------------------------------------------
            if case is "tt":
                print("\n****** TOP-N: {} X 2 (J-pop/K-pop) ******\n".format(top_n))
                words_ja = ja[:top_n]
                words_ko = ko[:top_n]
            # --------------------------------------------------------------------------------

            # *** Bottom-N vs. Bottom-N *** -------------------------------------------------
            if case is "bb":
                print("\n****** BOTTOM-N: {} X 2 (J-pop/K-pop) ******\n".format(top_n))
                words_ja = rev_ja[:top_n]
                words_ko = rev_ko[:top_n]
            # --------------------------------------------------------------------------------

            # *** Top-N vs. Bottom-N *** -------------------------------------------------
            if case is "tb":
                print("\n****** TOP-N (J-pop) {} & BOTTOM-N (K-pop) {} ******\n".format(top_n, top_n))
                words_ja = ja[:top_n]
                words_ko = rev_ko[:top_n]
            # --------------------------------------------------------------------------------

            # *** Bottom-N vs. Top-N *** -------------------------------------------------
            if case is "bt":
                print("\n****** BOTTOM-N (J-pop) {} & TOP-N (K-pop) {} ******\n".format(top_n, top_n))
                words_ja = rev_ja[:top_n]
                words_ko = ko[:top_n]
            # --------------------------------------------------------------------------------

            words = words_ja + words_ko
            print("# of selected words (uniq):", len(set(words)))
            result_n_w.append(len(set(words)))

            lyrics_ja_added = []
            for lyric in lyrics_ja:
                tmp = []
                for w in lyric:
                    # -----------------------------
                    # Select top-n/bottom-n J-pop words from the filtered J-pop lyrics data.
                    if w in words:
                        tmp.append(w)
                    # -----------------------------
                if tmp != []:
                    lyrics_ja_added.append(tmp)
            print("lyrics ja added:", len(lyrics_ja_added))

            lyrics_ko_added = []
            for lyric in lyrics_ko:
                tmp = []
                for w in lyric:
                    # -----------------------------
                    # Select top-n/bottom-n K-pop words from the filtered K-pop lyrics data.
                    if w in words:
                        tmp.append(w)
                    # -----------------------------
                if tmp != []:
                    lyrics_ko_added.append(tmp)
            print("lyrics ko added:", len(lyrics_ko_added))

            # Merge two lyrics data.

            lyrics_all_added = lyrics_ja_added + lyrics_ko_added

            label_ja = [1] * len(lyrics_ja_added)
            label_ko = [0] * len(lyrics_ko_added)
            label = label_ja + label_ko

            # Perform term frequency-index document frequency transformation.

            tfidf = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=lambda x: x)
            vect = tfidf.fit_transform(lyrics_all_added)
            print("# tfidf vect shape:", vect.shape)
            # print("# tfidf vect features:", tfidf.get_feature_names()[:3])

            num_clusters = 2  # Clusters J-pop lyrics data and K-pop lyrics data.

            ari_list = []

            # Experiment 5 clustering trials with 5 different fixed seeds.
            # This is done for fair comparison among different mode-2 values.

            # To save execution time, one trial experiment is conducted instead of five.
            # for i in range(5):
            for i in range(1):
                # Perform k-means clustering.

                km = KMeans(n_clusters=num_clusters, random_state=i)
                y_predict = km.fit_predict(vect)

                # Adjusted rand score is used to evaluate the clustering result.

                ari = adjusted_rand_score(y_predict, label)
                #print("trial_{}: ari={:.5f}".format(i + 1, ari))

                ari_list.append(ari)

            # Calculate the mean ARI performance of five trials.

            #mean_ari = float(sum(ari_list)) / max(len(ari_list), 1)

            if case is "tt":
                print("\n--- J-pop & K-pop CPD WORDS: TOP-{} & TOP-{} ---".format(top_n, top_n))

            if case is "bb":
                print("\n--- J-pop & K-pop CPD WORDS: BOTTOM-{} & BOTTOM-{} ---".format(top_n, top_n))

            if case is "tb":
                print("\n--- J-pop & K-pop CPD WORDS: TOP-{} & BOTTOM-{} ---".format(top_n, top_n))

            if case is "bt":
                print("\n--- J-pop & K-pop CPD WORDS: BOTTOM-{} & TOP-{} ---".format(top_n, top_n))

            #print("ARI: {:.5f}".format(round(mean_ari, 5)))
            print("ARI={:.5f}".format(round(ari, 5)))

            #result_ari.append(mean_ari)
            result_ari.append(round(ari, 5))

        # Save results to file.

        f_ari = "{}/ari_{}.csv".format(table_dir, case)
        with open(f_ari, "w") as f:
            writer = csv.writer(f)
            writer.writerows([result_ari])

        f_n_w = "{}/num_words_{}.csv".format(table_dir, case)
        with open(f_n_w, "w") as f:
            writer = csv.writer(f)
            writer.writerows([result_n_w])

def draw_line_graph():
    # Create 'fig' directory if there isn't any.

    fig_dir = "fig"
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)

    in_file_tfidf = "table/tfidf.txt"
    with open(in_file_tfidf,"r") as f:
        tfidf = f.read()
    data_tfidf = np.full((20,), np.round(float(tfidf), 5))

    in_file_tt = "table/ari_tt.csv"
    df_tt = pd.read_csv(in_file_tt, header=None)
    data_tt = np.round(df_tt.iloc[[0]].values[0], 5)

    in_file_bb = "table/ari_bb.csv"
    df_bb = pd.read_csv(in_file_bb, header=None)
    data_bb = np.round(df_bb.iloc[[0]].values[0], 5)

    in_file_tb = "table/ari_tb.csv"
    df_tb = pd.read_csv(in_file_tb, header=None)
    data_tb = np.round(df_tb.iloc[[0]].values[0], 5)

    in_file_bt = "table/ari_bt.csv"
    df_bt = pd.read_csv(in_file_bt, header=None)
    data_bt = np.round(df_bt.iloc[[0]].values[0], 5)

    t = arange(50, 1050, 50)

    plot(t, data_tt, linestyle="-", label="jako_both_TOP", marker="o")
    plot(t, data_bb, linestyle="--", label="jako_both_BOTTOM", marker="+")
    plot(t, data_tb, linestyle="-.", label="ja_TOP/ko_BOTTOM", marker="s")
    plot(t, data_bt, linestyle=":", label="ja_BOTTOM/ko_TOP", marker="x")
    plot(t, data_tfidf, linestyle="--", dashes=(5, 3), label="tf-idf")

    legend()

    xlabel('N Words (JA/KO)')
    ylabel('Adjusted Rand Index (ARI)')

    ylim(0.0, 1.0)

    title("K-Means Clustering With Various N Words")
    grid(True)
    savefig("fig/clustering_performance.png")
    show()
    plt.gcf().clear()

# Execute the below functions in a sequential manner.

#---------------------------------------
# Calculate the baseline performance of tfidf using all filtered words (i.e., 1,007 index words).

#baseline()

#---------------------------------------
# Calculate the top_n X top_n, top_n X bottom_n, bottom_n X top_n, bottom_n X bottom_n,
# J-pop X K-pop CPD lyrics word clustering performance using K-means clustering.

#top_x_bottom()

#---------------------------------------
# Draw a line graph of the experimental results.

#draw_line_graph()
