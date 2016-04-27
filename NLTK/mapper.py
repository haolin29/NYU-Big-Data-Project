#!/usr/bin/env python
#!/usr/bin/python
import sys
import os
import re
# import csv
# import zipfile
# import zipimport
# importer = zipimport.zipimporter('nltk.mod')
# Crypto = importer.load_module('Crypto')
# nltk = importer.load_module('nltk')
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

f = open("training_set.txt",'r')
sa = SentimentAnalyzer()
trainingset = []
for line in f:
    senti = line.split(",")[0]
    content = line[len(senti)+1:]
    tokens = nltk.word_tokenize(content.strip().lower())
    trainingset.append((tokens,senti))
all_words_neg = sa.all_words([mark_negation(doc) for doc in trainingset])
unigram_feats = sa.unigram_word_feats(all_words_neg,min_freq = 4)
sa.add_feat_extractor(extract_unigram_feats,unigrams=unigram_feats)
training_set = sa.apply_features(trainingset)
trainer = NaiveBayesClassifier.train
classifier = sa.train(trainer,training_set)


for line in sys.stdin:
    tweetWords=[]
    tweet= line.split(";")[4]
    words = tweet.split()
    for i in words:
        i = i.lower()
        i = i.strip('@#\'"?,.!')
        tweetWords.append(i)
    sentiment = sa.classify(tweetWords)
    print '%s\t%smuu' % (sentiment, "1")













# file2 = open('test.csv', 'r')
# reader2 = csv.reader(file2,delimiter=';',quotechar='|')
# new_rows_list = []
# for row in reader2:
#     tweetWords=[]
#     tweet= row[4]
#     words = tweet.split()
#     for i in words:
#         i = i.lower()
#         i = i.strip('@#\'"?,.!')
#         tweetWords.append(i)
#     sentiment = sa.classify(tweetWords)
#
#     new_row = [row[0], row[1], row[2],row[3],row[5],sentiment]
#     new_rows_list.append(new_row)
# file2.close()   # <---IMPORTANT
#
# # Do the writing
# file3 = open('test.csv', 'w+')
# writer = csv.writer(file3,delimiter=';',quotechar='|')
# writer.writerows(new_rows_list)
# file3.close()
# print "> Sentiment Saved..."
