# PlaynView-DistinctWordFinder

This code finds distinct lyrics words from K-pop/J-pop lyrics data using CP decomposition.

![](https://github.com/heeryoncho/playnview_distinctwordfinder/blob/master/docs/flow.png)


Please follow the instructions below to run the code:

## Requirements
This code has been tested under:
* Ubuntu 16.04
* Python 3.5

## List of Required Python Libraries
The following python libraries are required to run this code:
* pandas
* requests
* beautifulsoup4
* mecab-python3 (uses mecab-ipadic-neologd dictionary)
* konlpy
* gensim
* numpy
* tensorly
* scikit-learn
* matplotlib

## Downloading Data
You need to manually save the yearly top 100 ranking webpages (10 years worth) from a Korean music ranking site [https://www.melon.com/](https://www.melon.com/).

See instruction.txt located under the 'crawl_data > melon' directory.

## Reproducibility
To obtain consistent results, you need to set the PYTHONHASHSEED environment variable. You can do this through the command line interface as shown below,
```
$ PYTHONHASHSEED=0 python3 main_distinct_word_finder.py
```
or through PyCharm if you are using PyCharm. Go to the top menu 'Run', then 'Edit Configurations', then add the 'PYTHONHASHSEED' to the 'Environment variables'.


## YouTube
There is a YouTube demo of PlaynView-DistinctWordFinder in action at:
[https://youtu.be/cFlsN6oM55c](https://youtu.be/cFlsN6oM55c)

Please contact "heeryon.cho@gmail.com" if you have any questions.
