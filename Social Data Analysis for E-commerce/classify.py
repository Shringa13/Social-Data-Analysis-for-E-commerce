import sys
import time
import os
import json
import pandas as pd
from collections import defaultdict
from TwitterAPI import TwitterAPI
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import csv
import re
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


def afinn():
    url = urlopen('http://www2.compute.dtu.dk/~faan/data/AFINN.zip')
    zipfile = ZipFile(BytesIO(url.read()))
    afinn_file = zipfile.open('AFINN/AFINN-111.txt')
    
    afinn = dict()
    
    for line in afinn_file:
        parts = line.strip().split()
        if len(parts) == 2:
            afinn[parts[0].decode("utf-8")] = int(parts[1])
    return afinn

def tokenize(text):
    return re.sub('\W+', ' ', text.lower()).split()
 


def afinn_sentiment2(terms, afinn, verbose=False):
    pos = 0
    neg = 0
    for t in terms:
        if t in afinn:
            if verbose:
                print('\t%s=%d' % (t, afinn[t]))
            if afinn[t] > 0:
                pos += afinn[t]
            else:
                neg += -1 * afinn[t]
    return pos, neg	 
	
def main():
    searchQuery = ['flipkartsupport','AskeBay','AmazonHelp']
    positives = []
    negatives = []
    list_tweet =[]
    list_pos =[]
    list_neg =[]
    labels = []
    user =[]
    for i in searchQuery:
        with open(i+'.txt', 'r') as f:
            my_list = [line.rstrip('\n') for line in f]
        words = afinn()
        tokens = [tokenize(t) for t in my_list]

        for token_list, tweet in zip(tokens, my_list):
            pos, neg = afinn_sentiment2(token_list, words)
            if pos > neg:
                positives.append((tweet, pos, neg))
            elif neg > pos:
                negatives.append((tweet, pos, neg))
        #with open(i+"_sentiment.txt", 'w') as outfile:
        for tweet, pos, neg in sorted(positives, key=lambda x: x[1], reverse=True):
            list_tweet.append(tweet)
            list_pos.append(pos)
            list_neg.append(neg)
            labels.append("POSITIVE")
            user.append(i)
                #outfile.write("%s,%d,%d,%s\n" % (str(tweet).encode("utf-8"),pos,neg,"POSITIVE"))
        for tweet, pos, neg in sorted(negatives, key=lambda x: x[1], reverse=True):
            list_tweet.append(tweet)
            list_pos.append(pos)
            list_neg.append(neg)
            labels.append("NEGATIVE")
            user.append(i)
                #outfile.write("%s,%d,%d,%s\n" % (str(tweet).encode("utf-8"),pos,neg,"NEGATIIVE"))
        Final = {'Tweet':list_tweet,'Positive':list_pos,'Negative':list_neg,'Labels':labels,'user':user}
        df = pd.DataFrame(Final)
        df.to_csv('Sentiment.csv')
        

if __name__ == '__main__':
    main()