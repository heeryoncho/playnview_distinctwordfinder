from find_distinct_words import preprocess
from find_distinct_words import build
from find_distinct_words import experiment
from find_distinct_words import find
from find_distinct_words import review
import time

'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code executes the steps required for finding the 
K-pop/J-pop distinct lyrics words.

The steps are carried out as follows:

1. preprocess: performs tokenization and filtering of K-pop/J-pop lyrics words.

2. build: builds word2vec vectors and sorts lyrics words based on CP decomposition.

3. experiment: outputs a line graph showing effective n words used in clustering.

4. find: distinct lyrics words are found using the 'sorting method' and 'n' argument.

This code assumes that K-pop/J-pop lyrics texts are already available.
 
'''

#-----------------------------------------------
# STEP 1. PREPROCESS
#-----------------------------------------------

# Where the lyrics text files are saved.

lyrics_ja = "../crawl_data/lyrics_jp/jp_lyrics_verbose.csv"
lyrics_ko = "../crawl_data/lyrics_kr/kr_lyrics_verbose.csv"

# Tokenize J-pop/K-pop lyrics data.

preprocess.tokenize_ja(lyrics_ja)
preprocess.tokenize_ko(lyrics_ko)

# Check the content of the J-pop/K-pop lyrics word alignment dictionary.

preprocess.check_dictionary()

# Filter J-pop/K-pop lyrics data using the alignment dictionary.

preprocess.filter_lyrics()


#-----------------------------------------------
# STEP 2. BUILD
#-----------------------------------------------

# Build j-pop and k-pop word2vec vectors.

build.word2vec()

# Build CPD word list using fixed mode-3 value CP decomposition.

build.CPD_wordlist()


#-----------------------------------------------
# STEP 3. EXPERIMENT
#-----------------------------------------------

# Calculate the baseline performance of tfidf using all filtered words (i.e., 1,007 index words).

experiment.baseline()

# Calculate the top_n X top_n, top_n X bottom_n, bottom_n X top_n, bottom_n X bottom_n,
# J-pop X K-pop CPD lyrics word clustering performance using K-means clustering.

experiment.top_x_bottom()

print("\n============================================")
print("|   You will see a graph pop up.           |")
print("|   Please determine the word size and     |")
print("|   up/bottom of 'ja' and 'ko' words.      |")
print("============================================\n\n\n")

time.sleep(5)

# Draw a line graph of the experimental results and show it to the user.

experiment.draw_line_graph()

#-----------------------------------------------
# STEP 4. FIND
#-----------------------------------------------

# Based on the 'fig/clustering_performance.png', the user determines
# the size of n (integer) and
# the lyrics word sorting method (string: either 'top' or 'bottom') for each of the J-pop & K-pop.

# Ask the user, the number of words, up/bottom decision of 'ja' and 'ko' words.

n_words = input("Number of words?: ")
j_pop = input("J-pop (ja): top or bottom? Type 't' or 'b': ")
k_pop = input("K-pop (ko): top or bottom? Type 't' or 'b': ")

# The list of distinct words are saved under the 'result' directory.

find.distinct_words(int(n_words), j_pop, k_pop)
#find.distinct_words(300, 'b', 't')


#=====================================================================================================
# Optionally, the user can review the data statistics used in the application using the below function.

review.data_statistics()

