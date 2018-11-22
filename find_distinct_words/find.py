import os
import pickle
import pandas as pd
from tabulate import tabulate
from find_distinct_words import common_func
from find_distinct_words import sort_freq
import webbrowser


'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code sorts the distinct word lists according to the K-pop lyrics word frequency,
and saves the sorted distinct word lists into the 'result/result_ja/result_ko' folder.

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

    # Set the N words information based on the clustering results.

    n_words = n_words

    sort_label_ja = label_jpop
    sort_label_ko = label_kpop

    # Load CPD word list.

    ja, ko, neu = common_func.load_word_list()

    # Reverse K-pop & J-pop CPD words list.

    rev_ko = list(reversed(ko))
    rev_ja = list(reversed(ja))

    if sort_label_ko is 'b':
        ko = rev_ko

    if sort_label_ja is 'b':
        ja = rev_ja

    print("--------------------------------------------------------")
    words = set.union(set(ko[:n_words]), set(ja[:n_words]))
    print("# of total words (union):", len(words))

    # Load ja2ko_dictionary.
    jako_dict = pickle.load(open("dictionary/ja2ko_dict.p", 'rb'))
    koja_dict = {y: x for x, y in jako_dict.items()}

    # ----------------------------------------------------------------
    # Final K-pop/J-pop CPD word list is obtained by taking the
    # intersection of the nine cases of mode-3 value results.
    # ----------------------------------------------------------------

    print("\n==========================================")
    print("              FINAL WORDLIST              ")
    print("==========================================")

    u_ko = set(ko[:n_words])
    u_ja = set(ja[:n_words])
    u_common = set.intersection(u_ko, u_ja)
    u_words = set.union(u_ko, u_ja)

    print("# of KO words:", len(u_ko))
    print("# of JA words:", len(u_ja))
    print("# of COMMON words", len(u_common))
    print("# of UNION words (KO+JA):", len(u_words))

    # Save final distinct words (full) in pickle format for later use (See 'review()' function).
    with open("result/distinct_words_full.p", 'wb') as f:
        pickle.dump(list(u_words), f)

    u_ko_sans = u_ko - u_common
    u_ja_sans = u_ja - u_common
    u_words_sans = set.union(u_ko_sans, u_ja_sans)

    print("\n# of KO words (w/o common):", len(u_ko_sans))
    print("# of JA words (w/o common):", len(u_ja_sans))
    print("# of UNION words (KO+JA, w/o common):", len(u_words_sans))

    # Save final distinct words (minimum) in pickle format for later use (See 'review()' function).
    with open("result/distinct_words_minimum.p", 'wb') as f:
        pickle.dump(list(u_words_sans), f)

    sorted_u_ko_sans_k = []
    sorted_u_ko_sans_j = []

    sorted_u_ko_sans_k_n = []
    sorted_u_ko_sans_k_a = []
    sorted_u_ko_sans_k_v = []

    sorted_u_ko_sans_j_n = []
    sorted_u_ko_sans_j_a = []
    sorted_u_ko_sans_j_v = []

    for each_ko in ko[:n_words]:
        if each_ko in u_ko_sans:
            sorted_u_ko_sans_k.append(each_ko)
            if 'NNG' in each_ko or 'NNP' in each_ko:
                sorted_u_ko_sans_k_n.append(each_ko.replace(':NNG','').replace(':NNP','').replace(':VA','다').replace(':VV','다'))
            if 'VA' in each_ko:
                sorted_u_ko_sans_k_a.append(each_ko.replace(':NNG','').replace(':NNP','').replace(':VA','다').replace(':VV','다'))
            if 'VV' in each_ko:
                sorted_u_ko_sans_k_v.append(each_ko.replace(':NNG','').replace(':NNP','').replace(':VA','다').replace(':VV','다'))
            sorted_u_ko_sans_j.append(koja_dict[each_ko])
            if '名詞' in koja_dict[each_ko]:
                sorted_u_ko_sans_j_n.append(koja_dict[each_ko].replace(':名詞','').replace(':形容詞','').replace(':動詞',''))
            if '形容詞' in koja_dict[each_ko]:
                sorted_u_ko_sans_j_a.append(koja_dict[each_ko].replace(':名詞','').replace(':形容詞','').replace(':動詞',''))
            if '動詞' in koja_dict[each_ko]:
                sorted_u_ko_sans_j_v.append(koja_dict[each_ko].replace(':名詞','').replace(':形容詞','').replace(':動詞',''))

    with open('result/distinct_words_minimum_k_pop_ko.txt', 'w') as f:
        for each_ko in sorted_u_ko_sans_k:
            f.write("%s\n" % each_ko)

    with open('result/distinct_words_minimum_k_pop_ja.txt', 'w') as f:
        for each_ko in sorted_u_ko_sans_j:
            f.write("%s\n" % each_ko)

    sorted_u_ja_sans_k = []
    sorted_u_ja_sans_j = []

    sorted_u_ja_sans_k_n = []
    sorted_u_ja_sans_k_a = []
    sorted_u_ja_sans_k_v = []

    sorted_u_ja_sans_j_n = []
    sorted_u_ja_sans_j_a = []
    sorted_u_ja_sans_j_v = []

    for each_ja in ja[:n_words]:
        if each_ja in u_ja_sans:
            sorted_u_ja_sans_k.append(each_ja)
            sorted_u_ja_sans_k.append(each_ja)
            if 'NNG' in each_ja or 'NNP' in each_ja:
                sorted_u_ja_sans_k_n.append(each_ja.replace(':NNG','').replace(':NNP','').replace(':VA','다').replace(':VV','다'))
            if 'VA' in each_ja:
                sorted_u_ja_sans_k_a.append(each_ja.replace(':NNG','').replace(':NNP','').replace(':VA','다').replace(':VV','다'))
            if 'VV' in each_ja:
                sorted_u_ja_sans_k_v.append(each_ja.replace(':NNG','').replace(':NNP','').replace(':VA','다').replace(':VV','다'))
            sorted_u_ja_sans_j.append(koja_dict[each_ja])
            if '名詞' in koja_dict[each_ja]:
                sorted_u_ja_sans_j_n.append(koja_dict[each_ja].replace(':名詞','').replace(':形容詞','').replace(':動詞',''))
            if '形容詞' in koja_dict[each_ja]:
                sorted_u_ja_sans_j_a.append(koja_dict[each_ja].replace(':名詞','').replace(':形容詞','').replace(':動詞',''))
            if '動詞' in koja_dict[each_ja]:
                sorted_u_ja_sans_j_v.append(koja_dict[each_ja].replace(':名詞','').replace(':形容詞','').replace(':動詞',''))

    with open('result/distinct_words_minimum_j_pop_ko.txt', 'w') as f:
        for each_ja in sorted_u_ja_sans_k:
            f.write("%s\n" % each_ja)

    with open('result/distinct_words_minimum_j_pop_ja.txt', 'w') as f:
        for each_ja in sorted_u_ja_sans_j:
            f.write("%s\n" % each_ja)


    # Save results in Korean.

    common_func.save_distinct_words_ko(list(u_common), "common")
    common_func.save_distinct_words_ko(list(u_ko_sans), "k_pop")
    common_func.save_distinct_words_ko(list(u_ja_sans), "j_pop")

    # Output top-10/top-20 results in web browser.
    sort_freq.summary_ko()

    # Save results in Japanese.

    common_func.save_distinct_words_ja(list(u_common), "common")
    common_func.save_distinct_words_ja(list(u_ko_sans), "k_pop")
    common_func.save_distinct_words_ja(list(u_ja_sans), "j_pop")

    # Output top-10/top-20 results in web browser.
    sort_freq.summary_ja()


    # Based on CPD word list.

    df_korean = pd.DataFrame.from_dict({'K-POP-Noun':sorted_u_ko_sans_k_n,
                              'J-POP-Noun':sorted_u_ja_sans_k_n,
                              'K-POP-Adj':sorted_u_ko_sans_k_a,
                              'J-POP-Adj':sorted_u_ja_sans_k_a,
                              'K-POP-Verb':sorted_u_ko_sans_k_v,
                              'J-POP-Verb':sorted_u_ja_sans_k_v}, orient='index').T
    df_japanese = pd.DataFrame.from_dict({'K-POP-Noun':sorted_u_ko_sans_j_n,
                                'J-POP-Noun':sorted_u_ja_sans_j_n,
                                'K-POP-Adj':sorted_u_ko_sans_j_a,
                                'J-POP-Adj':sorted_u_ja_sans_j_a,
                                'K-POP-Verb':sorted_u_ko_sans_j_v,
                                'J-POP-Verb':sorted_u_ja_sans_j_v}, orient='index').T
    #print(df_korean.shape)
    #print(df_japanese.shape)

    df_korean = df_korean[['K-POP-Noun', 'J-POP-Noun', 'K-POP-Adj', 'J-POP-Adj', 'K-POP-Verb', 'J-POP-Verb']]
    df_japanese = df_japanese[['K-POP-Noun', 'J-POP-Noun', 'K-POP-Adj', 'J-POP-Adj', 'K-POP-Verb', 'J-POP-Verb']]

    df_korean = df_korean.where((pd.notnull(df_korean)), None)
    html_korean = tabulate(df_korean, headers='keys', tablefmt='html', showindex=False)

    with open('result/result_korean.html', 'w') as file:
        file.write(html_korean)

    path = 'file:///home/hcilab/Documents/OSS/playnview_distinctwordfinder/find_distinct_words/result/result_korean.html'
    webbrowser.get(using='google-chrome').open(path)

    df_japanese = df_japanese.where((pd.notnull(df_japanese)), None)
    html_japanese = tabulate(df_japanese, headers='keys', tablefmt='html', showindex=False)

    with open('result/result_japanese.html', 'w') as file:
        file.write(html_japanese)

    path = 'file:///home/hcilab/Documents/OSS/playnview_distinctwordfinder/find_distinct_words/result/result_japanese.html'
    webbrowser.get(using='google-chrome').open(path)



# Find distinct words using the following arguments:
# n words /int/: n is determined by the user after consulting
#                the 'fig/clustering_performance.png'
# sorting method /'top' or 'bottom'/: also determined using the figure.

#distinct_words(500, 'b', 't')


'''

/usr/bin/python3 /home/hcilab/Documents/OSS/playnview_distinctwordfinder/find_distinct_words/find.py
--------------------------------------------------------
# of total words (union): 545

==========================================
              FINAL WORDLIST              
==========================================
# of KO words: 300
# of JA words: 300
# of COMMON words 55
# of UNION words (KO+JA): 545

# of KO words (w/o common): 245
# of JA words (w/o common): 245
# of UNION words (KO+JA, w/o common): 490

----------------------------------------
     DISTINCT COMMON WORDS : KO    
----------------------------------------
matched_common: 55
split_common: 65

----------------------------------------
     DISTINCT K_POP WORDS : KO    
----------------------------------------
matched_k_pop: 245
split_k_pop: 277

----------------------------------------
     DISTINCT J_POP WORDS : KO    
----------------------------------------
matched_j_pop: 245
split_j_pop: 289

----------------------------------------
     DISTINCT COMMON WORDS : JA    
----------------------------------------
matched_common: 55
split_common: 70

----------------------------------------
     DISTINCT K_POP WORDS : JA    
----------------------------------------
matched_k_pop: 245
split_k_pop: 320

----------------------------------------
     DISTINCT J_POP WORDS : JA    
----------------------------------------
matched_j_pop: 245
split_j_pop: 334

Process finished with exit code 0

'''