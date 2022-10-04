"""
Created on Wed May 17 15:06:41 2019
@author: BBE - Brian Hogan
Purpose: ist652 Final Project
Objective: Generate New York State twitter traffic chatter to match to good,
bad, and ugly traffic days.
Method: have a Mongodb that keeps getting tweets dropped into by running the 
program for the different twitter handles. Data is then extracted to a dataframe
for analysis. 
"""
import tweepy   #necessary packages
import json
import pymongo
import pandas as pd
from bson.json_util import dumps  #from dn_fn.py for save & load to database

CONSUMER_KEY = 'GFuEK46tIlJc3CAZBSOir4uzv'  #Brian Hogan twitter keys...
CONSUMER_SECRET = 'sWsBF6S9EOPDsjgk38PcSYzTj
OAUTH_TOKEN = '989685004832792578-39uSCgyuEhOY
OAUTH_SECRET = 'zRm1pwVBQOYX4b8Wrab0PjWeMCLGxyJVX
"""asynch 8.4 twitter login        from:===> twitter_login.py   """
def oauth_login():
  auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
  auth.set_access_token(OAUTH_TOKEN,OAUTH_SECRET)
  tweepy_api = tweepy.API(auth)
  if (not tweepy_api):        #error out
      print ("Problem Connecting to API with OAuth")
  return tweepy_api  #api object to twitter functions
def appauth_login(): #login to twitter w extended rate limiting
  auth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
  #auth.set_access_token(OAUTH_TOKEN,OAUTH_SECRET) #needed for one test so put back in
  tweepy_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
  if (not tweepy_api):  #let user know if api error
      print ("Problem Connecting to API with AppAuth")
  return tweepy_api    #api object to twitter functions

"""asynch 8.4 - program connection test """
if __name__ == '__main__':  #test connection
  tweepy_api = oauth_login()
  print ("Twitter  Authorization OK :", tweepy_api)
  tweepy_api = appauth_login()
  print ("Twitter  Authorization OK :", tweepy_api) 

"""ASYNCH 8.4 from===> run_twitter_simple_search.py"""
def simple_search(api, query, max_results=20):  #ASYNCH 8.4
    # the first search initializes a cursor, stored in the metadata results,
  #   that allows next searches to return additional tweets
  search_results = [status for status in tweepy.Cursor(api.search, q=query).items(max_results)]  
  tweets = [tweet._json for tweet in search_results]
  return tweets

"""asynch dn_fn.py  """
def save_to_DB(DBname, DBcollection, data):    
    client = pymongo.MongoClient('localhost', 27017) #connect to server
    """change names to lowers case because they are not case senstitive
    and remove special characteers like hashtask and spaces   """  
    DBname = DBname.lower()
    DBname = DBname.replace('#', '')
    DBname = DBname.replace(' ', '')
    DBcollection = DBcollection.lower()
    DBcollection = DBcollection.replace('#', '')
    DBcollection = DBcollection.replace(' ', '')
    db = client[DBname]
    collection = db[DBcollection]   
    collection.insert_many(data)
    print("\nSaved", len(data), "documents to DB", DBname, DBcollection)

"""dn_fn.py  - used to get existing data; return as json objects"""
def load_from_DB(DBname, DBcollection):
    client = pymongo.MongoClient('localhost', 27017) 
    client.list_database_names   # ISSUE HERE W DEPRECTATION again...5-31-19
    db = client[DBname]
    collection = db[DBcollection]  #find collection and load docs  
    docs = collection.find()
    docs_bson = list(docs)
    docs_json_str = [dumps(doc) for doc in docs_bson]
    docs_json = [json.loads(doc) for doc in docs_json_str]
    return docs_json  

"""asynch 8.4 -                ==> run_twitter_simple_search_save.py  """
if __name__ == '__main__':
    """ask user for hashag, database and dbcollection so not hardcoded"""
    num_tweets = input("Enter max # of tweets to grab: ")
    num_tweets = int(num_tweets)
    query = input("Enter Twitter hashtag (#, @ etc): ")
    DBname = input("Enter mongodb name (this query doesnt overwrite old data): ")
    DBcollection = input("Please enter a name for the file within your database: ")
    
    api = appauth_login()  #login to thr api
    #api = oauth_login() <--uncomment if swtich to appauth to avoid rate limit

    result_tweets = simple_search(api, query, max_results=num_tweets)
    print ('Number of result tweets: ', len(result_tweets)) #let user know success
   
    save_to_DB(DBname, DBcollection, result_tweets)  #save to database
    
    """OK now that we have the tweets were going to do some counting"""
    print('Tweet summary statistics are next. Refer to the tweet-datatable.txt '\
          'output file in the folder run for full tweet dataset collected.') 
    #get results from mongo db
    tweet_results = load_from_DB(DBname.lower(), DBcollection.lower())
    tweet_df = pd.DataFrame() #initiate an empty dataframe to fill
    tweet_df['id']=[tweet['id'] for tweet in tweet_results] #collect data
    tweet_df['language']=[tweet['lang'] for tweet in tweet_results]
    tweet_df['location']=[tweet['user']['location'] for tweet in tweet_results]
    tweet_df['screen_name']=[tweet['user']['screen_name'] for tweet in tweet_results]
    tweet_df['followers']=[tweet['user']['followers_count']for tweet in tweet_results]
    tweet_df['tweet']=[tweet['text']for tweet in tweet_results]
    df2 = pd.DataFrame(tweet_df)
    #what data is provided to customer
    print("Tweet columns in the csv output reports include: ",df2.columns)
    
    #import summary statistics
    print("What are unique total counts, unique values, top values of tweets? :{}".format(df2.describe(include=['object'])))
    #this meta data could be parsed - need to learn how to execute
    print("Tweet import metadata :{}".format(df2.sum()))  #metadata of all tweets
    output_tweet_data = df2.describe(include=['object']) #output detail to csv
    output_tweet_data.to_csv("Final_project_Tweets_Dataframe_BBE.txt", index=True)
    #average followers
    print("What are the average total tweet followers :{}".format(df2.describe()))

    output_tweet_data = df2  #output the total tweet datatable
    output_tweet_data.to_csv("Final_project_Tweets_BBE.txt", index=True)
    
    """===WORD FREQUENCY=================="""
    import nltk  #for natural language modeling
    #nltk.download('stopwords')
#    client = pymongo.MongoClient('localhost', 27017) 
#    client.list_database_names()   # ISSUE HERE W DEPRECTATION again...5-31-19
#    #client.list_database_names()  
#    #project is 652(cant use - made bk, bkf the file)
#    """============="""
#    db = client.DBname #client.bk
#    db.collection_names()  #get the collection name
#    collection = DBcollection       #db.bk_f  #find collection and load docs 
#    """================"""
    """ THE FOLLOWING is what you use to go get the tweets and carry on"""
    docs = load_from_DB(DBname, DBcollection)

    doclist = [tweet for tweet in docs]
    #len(doclist)
    def print_tweet_data(tweets):    #sample loop to read through tweets
        for tweet in tweets:
            print('\nDate: ',tweet['text'])
            #print_tweet_data(doclist[:1])
    """important to build the message list"""
    msglist = [doc['text'] for doc in doclist if 'text' in doc.keys()]
    #len(msglist)
    """tokens are a summary of individual words"""
    all_tokens = [tok for msg in msglist for tok in nltk.word_tokenize(msg)]
    #len(all_tokens)
    #all_tokens[:10]
    msgtweet = nltk.FreqDist(all_tokens) #build the frequency of tokenized words
    #msgtweet.most_common(15)
    all_tokens = [tok.lower() for msg in msglist for tok in nltk.word_tokenize(msg)]
    #all_tokens[:10]
    nltk_stopwords = nltk.corpus.stopwords.words('english')#remove nonvalue add words
    #len(nltk_stopwords)
    import re
    def alpha_filter(w):
        pattern = re.compile('^[^a-z]+S')  #need to expand on filter for more
        if (pattern.match(w)):             #symbols
            return True
        else:
            return False
    token_list = [tok for tok in all_tokens if not alpha_filter(tok)]
    #token_list[:30]
    msgtweet = nltk.FreqDist(token_list)
    top_words=msgtweet.most_common(20) #words used most in the tweets
    #words={} #make a dictionary  ====>move to dictionary in future
    print("New York Twitter Traffic Chatter Most Common Words/Frequency")
    print("Note: more stop words identified for removal")
    for word, freq in top_words:   #print the most commone words
        print("Word:",word,freq)

"""======================================================================"""
"""TOKENIZATION & BINNING OF TOP WORDS FROM ALL THE TWEETS"""
"""======================================================================"""
"""ASYNCH 9.2=====GETTING THE TOP WORDS"""
import nltk  #for natural language modeling  #nltk.download('stopwords')
client = pymongo.MongoClient('localhost', 27017) 
client.list_database_names   # ISSUE HERE W DEPRECTATION again...5-31-19
#client.list_database_names()  #project is 652(cant use - made bk, bkf the file)
db = client.bk
db.collection_names()  #get the collection name
collection = db.bk_f  #find collection and load docs 
docs = collection.find()
doclist = [tweet for tweet in docs]
#len(doclist)
def print_tweet_data(tweets):    #sample loop to read through tweets
    for tweet in tweets:
        print('\nDate: ',tweet['text'])
#print_tweet_data(doclist[:1])
"""important to build the message list"""
msglist = [doc['text'] for doc in doclist if 'text' in doc.keys()]
#len(msglist)
"""tokens are a summary of individual words"""
all_tokens = [tok for msg in msglist for tok in nltk.word_tokenize(msg)]
#len(all_tokens)   #all_tokens[:10]
msgtweet = nltk.FreqDist(all_tokens) #build the frequency of tokenized words
#msgtweet.most_common(15)
all_tokens = [tok.lower() for msg in msglist for tok in nltk.word_tokenize(msg)]
#all_tokens[:10]
nltk_stopwords = nltk.corpus.stopwords.words('english')#remove nonvalue add words
#len(nltk_stopwords)
import re
def alpha_filter(w):
    pattern = re.compile('^[^a-z]+S')  #need to expand on filter for more
    if (pattern.match(w)):             #symbols
        return True
    else:
        return False
token_list = [tok for tok in all_tokens if not alpha_filter(tok)]
token_list[:30]
msgtweet = nltk.FreqDist(token_list)
top_words=msgtweet.most_common(100) #words used most in the tweets
#words={} #make a dictionary  ====>move to dictionary in future
print("New York Twitter Traffic Chatter Most Common Words/Frequency")
print("Note: more stop words identified for removal")
for word, freq in top_words:   #print the most commone words
        print("Word:",word,freq)
        
"""==================================================================="""
"""SENTIMMENT ANALYUSIS 9.3================================="""
"""==================================================================="""
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#this analyzer expects a list of text sentences
"""below is a variable"""
sentences =["This was really good book.","This movie was so bad.","I like to hate Michael Bay films, but I couldn't fault this on."]
sentences = msglist
#create the sentiment analyzer and run it on each sentence, printing a result
#showing the amount of positive, negative, and neutral. It also gives a compound
#score, which should be the overall sentiment, ranging from -1 (negative) to 
# +1 (positive).
""" generating polarity 0- """
sid=SentimentIntensityAnalyzer()
for sentence in sentences:
    print(sentence)
    ss=sid.polarity_scores(sentence)
    for k in sorted(ss):
        print('{0}:{1},'.format(k,ss[k]),end=' ') #single quote not a double


"""==================================================================="""
"""manual testing area=================================="""
"""================================================================="""
#import pymongo
#import pandas as pd
#from bson.json_util import dumps 
#import json
#DBname= "bk"                 #"june6"
#DBcollection= "bk_f"       #             "june6_f"
#tweet_results = load_from_DB(DBname.lower(), DBcollection.lower())
#tweet_df = pd.DataFrame() #initiate an empty dataframe to fill
#tweet_df['id']=[tweet['id'] for tweet in tweet_results] #collect data
#tweet_df['language']=[tweet['lang'] for tweet in tweet_results]
#tweet_df['location']=[tweet['user']['location'] for tweet in tweet_results]
#tweet_df['screen_name']=[tweet['user']['screen_name'] for tweet in tweet_results]
#tweet_df['followers']=[tweet['user']['followers_count']for tweet in tweet_results]
#tweet_df['tweet']=[tweet['text']for tweet in tweet_results]
#df2 = pd.DataFrame(tweet_df)
##what data is provided to customer
#print("Tweet columns in the csv output reports include: ",df2.columns)
    #                    id language          location  screen_name  followers
    #1  1135269902980407300       ru                     LvovCyprus         31
    #print(df2['followers']) #this is the proper indexingapproach
    
##import summary statistics
#print("What are unique total counts, unique values, top values of tweets? :{}".format(df2.describe(include=['object'])))
##this meta data could be parsed - need to learn how to execute
#print("Tweet import metadata :{}".format(df2.sum()))  #metadata of all tweets
#output_tweet_data = df2.describe(include=['object']) #output detail to csv
#output_tweet_data.to_csv("BBE_HW2_tweet_dataframe_describe_data.txt", index=True)
##average followers
#print("What are the average total tweet followers :{}".format(df2.describe()))
#
#output_tweet_data = df2  #output the total tweet datatable
#output_tweet_data.to_csv("BBE_HW2_tweet_datatable.txt", index=True)
#
##"""========================================================================"""
##"""TOKENIZATION & BINNING OF TOP WORDS FROM ALL THE TWEETS"""
#"""======================================================================"""
#"""ASYNCH 9.2=====GETTING THE TOP WORDS"""
#import nltk  #for natural language modeling  #nltk.download('stopwords')
#client = pymongo.MongoClient('localhost', 27017) 
#client.list_database_names   # ISSUE HERE W DEPRECTATION again...5-31-19
##client.list_database_names()  #project is 652(cant use - made bk, bkf the file)
#db = client.bk
#db.collection_names()  #get the collection name
#collection = db.bk_f  #find collection and load docs 
#docs = collection.find()
#doclist = [tweet for tweet in docs]
##len(doclist)
#def print_tweet_data(tweets):    #sample loop to read through tweets
#    for tweet in tweets:
#        print('\nDate: ',tweet['text'])
##print_tweet_data(doclist[:1])
#"""important to build the message list"""
#msglist = [doc['text'] for doc in doclist if 'text' in doc.keys()]
##len(msglist)
#"""tokens are a summary of individual words"""
#all_tokens = [tok for msg in msglist for tok in nltk.word_tokenize(msg)]
##len(all_tokens)   #all_tokens[:10]
#msgtweet = nltk.FreqDist(all_tokens) #build the frequency of tokenized words
##msgtweet.most_common(15)
#all_tokens = [tok.lower() for msg in msglist for tok in nltk.word_tokenize(msg)]
##all_tokens[:10]
#nltk_stopwords = nltk.corpus.stopwords.words('english')#remove nonvalue add words
##len(nltk_stopwords)
#import re
#def alpha_filter(w):
#    pattern = re.compile('^[^a-z]+S')  #need to expand on filter for more
#    if (pattern.match(w)):             #symbols
#        return True
#    else:
#        return False
#token_list = [tok for tok in all_tokens if not alpha_filter(tok)]
#token_list[:30]
#msgtweet = nltk.FreqDist(token_list)
#top_words=msgtweet.most_common(100) #words used most in the tweets
##words={} #make a dictionary  ====>move to dictionary in future
#print("New York Twitter Traffic Chatter Most Common Words/Frequency")
#print("Note: more stop words identified for removal")
#for word, freq in top_words:   #print the most commone words
#        print("Word:",word,freq)

msglist

#Word: @ 1950
#Word: : 475
#Word: https 249
#Word: the 226
#Word: . 217
#Word: trafficmanmatt 214
#Word: , 195
#Word: ! 170
#Word: rt 159
#Word: suzan916 116
#Word: to 110
#Word: a 104
#Word: frecklequeen45 102
#Word: dizzymom64 100
#Word: cab867 98
#Word: russelltob 96
#Word: and 80
#Word: i 79
#Word: of 78
#Word: gmgirl63 76
#Word: # 74
#Word: donzie1960 74
#Word: on 73
#Word: nysthruway 71
#Word: maryl1973 64
#Word: jeff3200 64
#Word: at 60
#Word: exit 57
#Word: in 56
#Word: for 54
#Word: you 49
#Word: is 47
#Word: ’ 47
#Word: ? 46
#Word: was 41
#Word: wendyan622… 40
#Word: this 38
#Word: 511nyalbany 38
#Word: mctarfu19611 36
#Word: it 35
#Word: mets 35
#Word: ; 33
#Word: from 32
#Word: kbgriffie 32
#Word: be 31
#Word: ) 31
#Word: ... 31
#Word: what 30
#Word: with 29
#Word: my 29
#Word: s 29
#Word: traffic 28
#Word: just 28
#Word: jasonnym 28
#Word: lisalgm1 28
#Word: thruwaytraffic 25
#Word: ( 24
#Word: wnyt 24
#Word: nbamlb 24
#Word: near 22
#Word: that 21
#Word: your 21
#Word: me 20
#Word: … 20
#Word: & 20
#Word: amp 20
#Word: he 20
#Word: tractor 20
#Word: trailer 20
#Word: marcelmyrick70 20
#Word: cynicalmike 20
#Word: carebear_53 20
#Word: fire 19
#Word: nytrafficbureau 19
#Word: here 19
#Word: - 19
#Word: 's 18
#Word: all 18
#Word: have 18
#Word: bridge 18
#Word: who 18
#Word: carebear_53… 18
#Word: left 17
#Word: over 17
#Word: susankinsella1 17
#Word: by 16
#Word: enjoy 16
#Word: out 15
#Word: thruway 15
#Word: falcon 15
#Word: new 15
#Word: johncraigwnyt 15
#Word: gomets01 15
#Word: msl20174 15
#Word: nb 14
#Word: closed 14
#Word: day 14
#Word: today 14
#Word: been 14
#Word: 21a 14










   