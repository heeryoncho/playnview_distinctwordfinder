# -*- coding: utf-8 -*-

import pandas as pd
from tabulate import tabulate
import webbrowser

'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code compares and ouputs the distinct word result in html file 
(chrome window pops up) using two languages, Japanese and Korean:

Note that the words are sorted according to the word frequency of the 
given country's lyrics data (from large fequency to small). 

- Comparison of top-20 K-pop, J-pop and Common nouns.

- Comparison of top-20 K-pop, J-pop and Common adjectives.

- Comparison of top-20 K-pop, J-pop and Common verbs. 

'''

def summary_ko():
    top_n = 30
    noun_ja = pd.read_csv("result_ko/distinct_j_pop_NNG.csv", header=None)
    noun_ja = noun_ja.iloc[:top_n, 0].str.replace(':NNG', '')

    noun_ko = pd.read_csv("result_ko/distinct_k_pop_NNG.csv", header=None)
    noun_ko = noun_ko.iloc[:top_n, 0].str.replace(':NNG', '')

    adj_ja = pd.read_csv("result_ko/distinct_j_pop_VA.csv", header=None)
    adj_ja = adj_ja.iloc[:top_n, 0].str.replace(':VA', '다')

    adj_ko = pd.read_csv("result_ko/distinct_k_pop_VA.csv", header=None)
    adj_ko = adj_ko.iloc[:top_n, 0].str.replace(':VA', '다')

    verb_ja = pd.read_csv("result_ko/distinct_j_pop_VV.csv", header=None)
    verb_ja = verb_ja.iloc[:top_n, 0].str.replace(':VV', '다')

    verb_ko = pd.read_csv("result_ko/distinct_k_pop_VV.csv", header=None)
    verb_ko = verb_ko.iloc[:top_n, 0].str.replace(':VV', '다')

    noun_common = pd.read_csv("result_ko/distinct_common_NNG.csv", header=None)
    noun_common = noun_common.iloc[:top_n, 0].str.replace(':NNG', '')

    adj_common = pd.read_csv("result_ko/distinct_common_VA.csv", header=None)
    adj_common = adj_common.iloc[:top_n, 0].str.replace(':VA', '다')

    verb_common = pd.read_csv("result_ko/distinct_common_VV.csv", header=None)
    verb_common = verb_common.iloc[:top_n, 0].str.replace(':VV', '다')

    summary = pd.concat([noun_ko, noun_ja, adj_ko, adj_ja, verb_ko, verb_ja,
                         noun_common, adj_common, verb_common], axis=1,
                        keys=['K-POP-Noun', 'J-POP-Noun', 'K-POP-Adj', 'J-POP-Adj',
                              'K-POP-Verb', 'J-POP-Verb', 'NEU_Noun', 'NEU-Adj', 'NEU-Verb'])
    summary = summary.where((pd.notnull(summary)), None)
    html = tabulate(summary, headers='keys', tablefmt='html', showindex=False)

    with open('result_ko/result_ko_freq_considered.html', 'w') as file:
        file.write(html)

    path = 'file:///home/hcilab/Documents/OSS/playnview_distinctwordfinder/find_distinct_words/result_ko/result_ko_freq_considered.html'
    webbrowser.get(using='google-chrome').open(path)

#summary_ko()

def summary_ja():
    top_n = 30
    noun_ja = pd.read_csv("result_ja/distinct_j_pop_noun.csv", header=None)
    noun_ja = noun_ja.iloc[:top_n, 0].str.replace(':名詞', '')

    noun_ko = pd.read_csv("result_ja/distinct_k_pop_noun.csv", header=None)
    noun_ko = noun_ko.iloc[:top_n, 0].str.replace(':名詞', '')

    adj_ja = pd.read_csv("result_ja/distinct_j_pop_adjective.csv", header=None)
    adj_ja = adj_ja.iloc[:top_n, 0].str.replace(':形容詞', '')

    adj_ko = pd.read_csv("result_ja/distinct_k_pop_adjective.csv", header=None)
    adj_ko = adj_ko.iloc[:top_n, 0].str.replace(':形容詞', '')

    verb_ja = pd.read_csv("result_ja/distinct_j_pop_verb.csv", header=None)
    verb_ja = verb_ja.iloc[:top_n, 0].str.replace(':動詞', '')

    verb_ko = pd.read_csv("result_ja/distinct_k_pop_verb.csv", header=None)
    verb_ko = verb_ko.iloc[:top_n, 0].str.replace(':動詞', '')

    noun_common = pd.read_csv("result_ja/distinct_common_noun.csv", header=None)
    noun_common = noun_common.iloc[:top_n, 0].str.replace(':名詞', '')

    adj_common = pd.read_csv("result_ja/distinct_common_adjective.csv", header=None)
    adj_common = adj_common.iloc[:top_n, 0].str.replace(':形容詞', '')

    verb_common = pd.read_csv("result_ja/distinct_common_verb.csv", header=None)
    verb_common = verb_common.iloc[:top_n, 0].str.replace(':動詞', '')

    summary = pd.concat([noun_ko, noun_ja, adj_ko, adj_ja, verb_ko, verb_ja,
                         noun_common, adj_common, verb_common], axis=1,
                        keys=['K-POP-Noun', 'J-POP-Noun', 'K-POP-Adj', 'J-POP-Adj',
                              'K-POP-Verb', 'J-POP-Verb', 'NEU_Noun', 'NEU-Adj', 'NEU-Verb'])
    summary = summary.where((pd.notnull(summary)), None)
    html = tabulate(summary, headers='keys', tablefmt='html', showindex=False)

    with open('result_ja/result_ja_freq_considered.html', 'w') as file:
        file.write(html)

    path = 'file:///home/hcilab/Documents/OSS/playnview_distinctwordfinder/find_distinct_words/result_ja/result_ja_freq_considered.html'
    webbrowser.get(using='google-chrome').open(path)

#summary_ja()