from creds import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

import tweepy
from textblob import TextBlob
from tqdm import tqdm

def authorize():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    try:
        api.verify_credentials()
        print("Authentication OK")

    except:
        print("Error during authentication")
        
    return api

def get_trends(api):
    tweets_ignored=0
    trends_result = api.trends_place(23424975)
    trend_list=list()
    for trend in trends_result[0]["trends"]:
        try:
            tr=trend["name"]
            trend_list.append(tr)
        except:
            tweets_ignored+=1
    print('\n\n\tNo of trends found: ',len(trend_list))        
    print('\tCertain tweets are ignored due to incompatibility.\n\tNo of tweets ignored are: ',tweets_ignored)
    return trend_list

def get_tweets(api,trend,count):
    MAX_TWEETS=count
    tweets=[]
    for tweet in tweepy.Cursor(api.search, q='#bmw', rpp=100).items(MAX_TWEETS):
        tweets.append(tweet.text)
    return tweets



def getTrendSentiment(no_of_tweets):
    api=authorize()
    print("Getting Trends")
    trends=get_trends(api)
    print("Getting tweets of each trend")
    trend_tweets={}
    for trend in tqdm(trends):
        tweets_list=get_tweets(api=api,trend=trend,count=no_of_tweets)
        trend_tweets[trend]=tweets_list
    print('Getting sentiment of each trend')
    trends_sentiment={}
    for trend,tweets in tqdm(trend_tweets.items()):
        positive=0
        negative=0
        neutral=0
        for tweet in tweets:
            text=TextBlob(tweet)
            sentiment=text.sentiment.polarity
            if sentiment>0:positive+=1
            elif sentiment<0:negative+=1
            else:neutral+=1

        trends_sentiment[trend]={'pos':positive,'neu':neutral,'neg':negative}
    return trends_sentiment
