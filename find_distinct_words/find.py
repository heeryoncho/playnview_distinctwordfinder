import os
import pickle
from find_distinct_words import common_func

'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code sorts the distinct word lists according to the K-pop lyrics word frequency,
and saves the sorted distinct word lists into the 'result' folder.

The following arguments should be specified:

--- n_words : /int/ the number of lyrics words that outperforms the baseline tfidf.
              this number is determined by 'fig/clustering_performance.png' line graph.

--- label_jpop : /'top' or 'bottom'/ the method that returned the best 
                 J-pop clustering performance based on the 
                 'fig/clustering_performance.png'.

--- label_kpop : /'top' or 'bottom'/ the method that returned the best 
                 K-pop clustering performance based on the  
                 'fig/clustering_performance.png'.
'''

'''

|+++++++++++++++++++++++++++++++++++++++++++++++++|
| distinct_words(n_words, label_jpop, label_kpop) |
|+++++++++++++++++++++++++++++++++++++++++++++++++|

load filtered J-pop & K-pop lyrics data.

'''

def distinct_words(n_words, label_jpop, label_kpop):
    # Create 'result' directory if there isn't any.

    result_dir = "result"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # Container for the final distinct K-pop & J-pop words.

    final_ko = []
    final_ja = []

    # Set the N words information based on the clustering results.

    n_words = n_words

    sort_label_ja = label_jpop
    sort_label_ko = label_kpop

    # The intersection of all nine cases of mode-3 values are taken to obtain
    # the final distinct K-pop & J-pop lyrics words.

    for w in range(1, 10):
        weight = "0.{}-0.{}-0.0".format(w, (10 - w))

        # Load CPD word list.

        ja, ko, neu = common_func.load_word_list(weight)

        # Reverse K-pop & J-pop CPD words list.

        rev_ko = list(reversed(ko))
        rev_ja = list(reversed(ja))

        if sort_label_ko is 'bottom':
            ko = rev_ko

        if sort_label_ja is 'bottom':
            ja = rev_ja

        final_ko.append(set(ko[:n_words]))
        final_ja.append(set(ja[:n_words]))

    print("--------------------------------------------------------")
    words = set.union(set(ko[:n_words]), set(ja[:n_words]))
    print("# of total words (union):", len(words))

    # ----------------------------------------------------------------
    # Final K-pop/J-pop CPD word list is obtained by taking the
    # intersection of the nine cases of mode-3 value results.
    # ----------------------------------------------------------------

    print("\n\n==========================================")
    print("              FINAL WORDLIST              ")
    print("==========================================")

    u_ko = set.intersection(*final_ko)
    u_ja = set.intersection(*final_ja)
    u_common = set.intersection(u_ko, u_ja)
    u_words = set.union(u_ko, u_ja)

    # Save final distinct words in pickle format for later use (See 'review()' function).
    with open("result/distinct_words.p", 'wb') as f:
        pickle.dump(list(u_words), f)

    print("# of KO words:", len(u_ko))
    print("# of JA words:", len(u_ja))
    print("# of COMMON words", len(u_common))
    print("# of UNION words (KO+JA):", len(u_words))

    common_func.save_distinct_words(list(u_common), "common")

    u_ko_sans = u_ko - u_common
    u_ja_sans = u_ja - u_common
    u_words_sans = set.union(u_ko_sans, u_ja_sans)

    print("# of KO words (w/o common):", len(u_ko_sans))
    print("# of JA words (w/o common):", len(u_ja_sans))
    print("# of UNION words (KO+JA, w/o common):", len(u_words_sans))

    common_func.save_distinct_words(list(u_ko_sans), "k_pop")
    common_func.save_distinct_words(list(u_ja_sans), "j_pop")


# Find distinct words using the following arguments:
# n words /int/: n is determined by the user after consulting
#                the 'fig/clustering_performance.png'
# sorting method /'top' or 'bottom'/: also determined using the figure.

distinct_words(300, 'bottom', 'top')


'''
/usr/bin/python3 /home/hcilab/Documents/OSS/playnview/find_distinct_words/find.py
--------------------------------------------------------
# of total words (union): 555


==========================================
              FINAL WORDLIST              
==========================================
# of KO words: 300
# of JA words: 299
# of COMMON words 44
# of UNION words (KO+JA): 555

----------------------------------------
     DISTINCT COMMON WORDS     
----------------------------------------
matched_common: 44
split_common: 54
# of KO words (w/o common): 256
# of JA words (w/o common): 255
# of UNION words (KO+JA, w/o common): 511

----------------------------------------
     DISTINCT K_POP WORDS     
----------------------------------------
matched_k_pop: 256
split_k_pop: 285

----------------------------------------
     DISTINCT J_POP WORDS     
----------------------------------------
matched_j_pop: 255
split_j_pop: 300

Process finished with exit code 0
'''