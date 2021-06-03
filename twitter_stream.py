import tweepy
import time as t
import datetime as dt
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# Input your keys from .env file
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


# NOTE: This method used for searching tweets
def searchTweets(api):
    for tweet in tweepy.Cursor(api.search,
                               q="Bitcoin",
                               tweet_mode='extended',
                               count=100,
                               lang="en",
                               since="2017-04-03").items():
        print('@' + tweet.user.screen_name, tweet.created_at, tweet.full_text)


#NOTE: This method and class is used for streaming real-time tweets
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            print('###BEGIN_EXTENDED###\n',
                  '@' + status.user.screen_name,
                  status.created_at,
                  status.extended_tweet['full_text'],
                  '\n ###END_EXTENDED###')
        except:
            try:
                print('###BEGIN_RTFULL###\n',
                      '@' + status.user.screen_name,
                      status.created_at,
                      status.retweeted_status.extended_tweet['full_text'],
                      '\n ###END_RTFULL###')
            except:
                try:
                    print('###BEGIN_TEXT###\n',
                          '@' + status.user.screen_name,
                          status.created_at,
                          status.text,
                          '\n ###END_TEXT###')
                except:
                    print('###BEGIN_EXCEPT###\n',
                          status,
                          '\n###END_EXCEPT')
        # try:
        #     print('@' + status.user.screen_name,
        #           status.created_at,
        #           '###RT_EXTENDED###',
        #           status.extended_tweet.full_text,
        #           status)
        # except:
        #     try:
        #         print('@' + status.user.screen_name,
        #         status.created_at,
        #         '###RT###',
        #         status.retweeted_status.full_text,
        #               status)
        #     except:
        #         print('@' + status.user.screen_name,
        #               status.created_at,
        #               '###TEXT###',
        #               status.text,
        #               status)
    def on_error(self, status_code):
        time = dt.datetime.utcnow()
        print("Tweepy: at time=%s an error occured. It is going to reconnect with back-off" % (time))


def streamTweets(api):
    # override tweepy.StreamListener to add logic to on_status
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended', include_entites=True)
    myStream.filter(track=['bitcoin', 'cryptocurrency'], languages=['en'])


streamTweets(api)
