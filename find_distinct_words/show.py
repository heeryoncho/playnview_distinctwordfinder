# -*- coding: utf-8 -*-

import pandas as pd
from tabulate import tabulate
import webbrowser

'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code summarizes and prints the distinct word result output:

- Comparison of top-20 K-pop, J-pop and Common nouns.

- Comparison of top-10 K-pop, J-pop and Common adjectives.

- Comparison of top-10 K-pop, J-pop and Common verbs. 

'''

def summary():
    noun_ja = pd.read_csv("result_ko/distinct_j_pop_NNG.csv", header=None)
    noun_ja = noun_ja.iloc[:20, 0].str.replace(':NNG', '')

    noun_ko = pd.read_csv("result_ko/distinct_k_pop_NNG.csv", header=None)
    noun_ko = noun_ko.iloc[:20, 0].str.replace(':NNG', '')

    adj_ja = pd.read_csv("result_ko/distinct_j_pop_VA.csv", header=None)
    adj_ja = adj_ja.iloc[:20, 0].str.replace(':VA', '다')

    adj_ko = pd.read_csv("result_ko/distinct_k_pop_VA.csv", header=None)
    adj_ko = adj_ko.iloc[:20, 0].str.replace(':VA', '다')

    verb_ja = pd.read_csv("result_ko/distinct_j_pop_VV.csv", header=None)
    verb_ja = verb_ja.iloc[:20, 0].str.replace(':VV', '다')

    verb_ko = pd.read_csv("result_ko/distinct_k_pop_VV.csv", header=None)
    verb_ko = verb_ko.iloc[:20, 0].str.replace(':VV', '다')

    noun_common = pd.read_csv("result_ko/distinct_common_NNG.csv", header=None)
    noun_common = noun_common.iloc[:20, 0].str.replace(':NNG', '')

    adj_common = pd.read_csv("result_ko/distinct_common_VA.csv", header=None)
    adj_common = adj_common.iloc[:20, 0].str.replace(':VA', '다')

    verb_common = pd.read_csv("result_ko/distinct_common_VV.csv", header=None)
    verb_common = verb_common.iloc[:20, 0].str.replace(':VV', '다')

    summary = pd.concat([noun_ko, noun_ja, adj_ko, adj_ja, verb_ko, verb_ja,
                         noun_common, adj_common, verb_common], axis=1,
                        keys=['Noun_ko', 'Noun_ja', 'Adj_ko', 'Adj_ja', 'Verb_ko', 'Verb_ja',
                              'Common_noun', 'Common_adj', 'Common_verb'])
    summary = summary.where((pd.notnull(summary)), None)
    html = tabulate(summary, headers='keys', tablefmt='html', showindex=False)

    with open('result/result.html', 'w') as file:
        file.write(html)

    path = 'file:///home/hcilab/Documents/OSS/playnview_distinctwordfinder/find_distinct_words/result/result.html'
    webbrowser.open(path)

summary()