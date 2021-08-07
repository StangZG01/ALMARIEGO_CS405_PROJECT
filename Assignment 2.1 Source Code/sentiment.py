from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from textblob import TextBlob
from tweepy import OAuthHandler
from tweepy import Stream

 
import twitter_credentials
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re


search_term = 'stocks'
tweet_amount = 300

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def get_search_results(self, search_term, lang, num_tweets):
        tweets = []
        for tweet in Cursor(api.search, q=search_term,lang=lang).items(num_tweets):
            tweets.append(tweet)
        return tweets


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0.00:
            return 1
        elif analysis.sentiment.polarity == 0.00:
            return 0
        elif analysis.sentiment.polarity < 0.00:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

 
if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    search_term = 'vaccination'
    tweet_amount = 200
    lang = 'en'

    api = twitter_client.get_twitter_client_api()
  
    tweets = twitter_client.get_search_results(search_term=search_term, lang = lang, num_tweets=tweet_amount)

    df = tweet_analyzer.tweets_to_data_frame(tweets)

    positive = 0
    neutral = 0
    negative = 0
    polarity = 0

    for tweet in df['tweets']:
        analysis = TextBlob(tweet_analyzer.clean_tweet(tweet))
    
        tweet_polarity = analysis.polarity
        if tweet_polarity > 0.00:
            positive += 1
        elif tweet_polarity < 0.00:
            negative += 1
        elif tweet_polarity == 0.00:
            neutral += 1
        polarity += analysis.polarity


    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    
    print(df.head(100))

    sum = positive + negative + neutral

    y = np.array([positive/sum, negative/sum, neutral/sum])
    mylabels = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    plt.pie(y, labels = mylabels, autopct='%1.2f%%')
    plt.title("How negative or positive most Filipino netizen \n" + "about the vaccination campaigns of the government?", bbox={'facecolor':'0.9', 'pad':6})
    plt.show()