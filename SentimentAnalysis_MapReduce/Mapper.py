#!/share/apps/python/2.7.11/bin/python

import sys
import os
import re

import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
f = open("training_set.txt",'r')
sa = SentimentAnalyzer()
trainingset = []
for line in f:
    senti = line.split(",")[0]
    content = line[len(senti)+1:]
    tokens = word_tokenize(content.rstrip())
    trainingset.append((tokens,senti))
all_words_neg = sa.all_words([mark_negation(doc) for doc in trainingset])
unigram_feats = sa.unigram_word_feats(all_words_neg,min_freq = 4)
sa.add_feat_extractor(extract_unigram_feats,unigrams=unigram_feats)
training_set = sa.apply_features(trainingset)

for line in sys.stdin:
    if "username" in line:
        continue

    tweetWords=[]
    tweet= line.split(";")[4]
    likes = line.split(";")[3]
    likes = int(likes)
    if likes==0:
        num=1
    else:
        num = 1+likes

    words = tweet.split()
    for i in words:
        i = i.lower()
        i = i.strip('@#\'"?,.!')
        tweetWords.append(i)
    sentiment = sa.classify(tweetWords)
    print '%s\t%s' % (sentiment, str(num))

