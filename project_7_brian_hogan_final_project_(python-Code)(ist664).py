"""
Created on Mon Dec 16 14:05:51 2019
@author: BBE
Class: ist664 Syracuse University Professor McCracken
DataSet: Class Final Project Twitter datasets
PUrpose: 
   The program is a combination of several class programs that will have use
   Natural language processing sentiment evaluation techniques to assess a
   Twitter data file, use NLTK Naive Bayes to classify and train feature sets.
   Results also will incorporate cross-validation and run a range of
   experiments with different feature functions.
"""
import os
import sys
import nltk
from nltk.tokenize import TweetTokenizer
os.getcwd()  #"C:\Users\17574\aDATA\camelot_grammar.cfg"

#=> Step-0: Import Data

#def processtweets(dirPath,limitStr):
  # convert the limit argument from a string to an int
limitStr = 10
limit = int(limitStr)

twtokenizer = TweetTokenizer()    # initialize NLTK built-in tweet tokenizer
  
os.chdir('C:\\Users\\17574\\Desktop\\ist664+NLP\\WK+x+Final+Project\\finalproject_DATA\\SemEval2014TweetData\\corpus')  
f = open('./downloaded-tweeti-b-dist.tsv', 'r')
  # loop over lines in the file and use the first limit of them
  #    assuming that the tweets are sufficiently randomized
tweetdata = []
limit = 10
for line in f:
    if (len(tweetdata) < limit):
        #remove final end of line character
        line = line.strip()
          # each line has 4 items separated by tabs
          # ignore the tweet and user ids, and keep the sentiment and tweet text
        tweetdata.append(line.split('\t')[2:4])
  
for tweet in tweetdata[:10]:
    print (tweet)
  
tweetdocs = []    # create list of tweet documents as (list of words, label)
  # add all the tweets except the ones whose text is Not Available
  for tweet in tweetdata:
    if (tweet[1] != 'Not Available'):
      # run the tweet tokenizer on the text string - returns unicode tokens, so convert to utf8
      tokens = twtokenizer.tokenize(tweet[1])

      if tweet[0] == '"positive"':
        label = 'pos'
      else:
        if tweet[0] == '"negative"':
          label = 'neg'
        else:          # labels are condensed to just 3:  'pos', 'neg', 'neu'
          if (tweet[0] == '"neutral"') or (tweet[0] == '"objective"') or (tweet[0] == '"objective-OR-neutral"'):
            label = 'neu'
          else:
            label = ''
      tweetdocs.append((tokens, label))

for tweet in tweetdocs[:10]: #this has grabbed the data file+tokens + rating
    print (tweet)  
    #(['Gas', 'by', 'my', 'house', 'hit', '$', '3.39', '!', '!', '!', "I'm", 
        #'going', 'to', 'Chapel', 'Hill', 'on', 'Sat', '.', ':)'], 'pos')
    #(['Theo', 'Walcott', 'is', 'still', 'shit', ',', 'watch', 'Rafa', 'and', 
        #'Johnny', 'deal', 'with', 'him', 'on', 'Saturday', '.'], 'neg')
        

  
""" BBE working here
    possibly filter tokens
  # continue as usual to get all words and create word features
  # feature sets from a feature definition function
  # train and test a classifier
  # show most informative features  """


























