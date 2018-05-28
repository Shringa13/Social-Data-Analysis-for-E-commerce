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


consumer_key = 'kRcA4PZZVD9GGbwvYjYhDJMsM'
consumer_secret = 'CjQwb0XoNzztmthAOyitH6b7XdtsfRCOWNGXT5yZC6DViu79S4'
access_token = '771404469372203008-wl3etEl3nCGL0stP2DRrc5JZEZaUoT3'
access_token_secret = 'igtSaHYD7VZrmUlvYSaaaTgxh2BrinaQHdWXQilmYtuKF'



def robust_request(twitter, resource, params, max_tries=5):

    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        elif request.status_code == 401:
            print('not authorized to view tweets')
        else:
            print(request.status_code)
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)

def main():

    twitter =TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
    searchQuery = ['flipkartsupport','AskeBay','AmazonHelp']
    maxTweets = 1500
    tweetsPerQry = 1000 
    userids=[]
    follows=[]

    for i in searchQuery:
        User_id = robust_request(twitter,'users/show', {'screen_name':i})
        Followers_id = robust_request(twitter,'followers/ids', {'screen_name':i})
        for user in User_id:
            for follower in Followers_id:
                follows.append(follower)
                userids.append(user['id'])
        sinceId = None
        max_id = -1
        tweetCount = 0
        with open(i+".txt", 'w') as outfile:
            while tweetCount < maxTweets:
                try:
                    if (max_id <= 0):
                        if (not sinceId):                           
                            new_tweets = robust_request(twitter,'search/tweets', {'q':i,'count':tweetsPerQry,'lang':'en'})                
                        else:                            
                            new_tweets = robust_request(twitter,'search/tweets', {'q':i,'count':tweetsPerQry,'since_id':sinceId,'lang':'en'})
                    else:
                        if (not sinceId):                           
                            new_tweets = robust_request(twitter,'search/tweets', {'q':i,'count':tweetsPerQry,'max_id':str(max_id - 1),'lang':'en'})
                        else:                            
                            new_tweets = robust_request(twitter,'search/tweets', {'q':i,'count':tweetsPerQry,'max_id':str(max_id - 1),'since_id':sinceId,'lang':'en'})
                    if not new_tweets:
                        print("No more tweets found")
                        break
                    counter=0
                    #new_tweets = robust_request(twitter,'search/tweets', {'q':i,'count':tweetsPerQry})
                    for tweet in new_tweets:
                        if tweet['user']['screen_name']!= i:
                            outfile.write("%s\n" % str(tweet['text']).encode("utf-8"))
                            counter=counter+1
                    tweetCount += counter
                except:
                    # Just exit if any error
                    print("some error : ")
                    break
        #print(str(tweets).encode("utf-8"))
    raw_data={'userids':userids,'follows':follows}
    df = pd.DataFrame(raw_data)
    df.to_csv('Followers.csv')
    
if __name__ == '__main__':
    main()