import praw#import library
import pprint
import json
import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
key = os.environ.get("FOREX_KEY")

if not os.path.exists('reddit_data'):
	os.makedirs('reddit_data')

client_id=os.environ.get('REDDIT_CLIENT_ID')
client_secret=os.environ.get('REDDIT_CLIENT_SECRET')
password=os.environ.get('REDDIT_PASSWORD')
user_agent=os.environ.get('REDDIT_USER_AGENT')
username=os.environ.get('REDDIT_USERNAME')

reddit = praw.Reddit(client_id= client_id, #authentication step
                     client_secret= client_secret,
                     password= password,
                     user_agent= user_agent,
                     username= username)

print(reddit.user.me()) #check authentication                     

#List of subreddits that we are interested in.
sub_list = ["Cryptocurrency", "Bitcoin", "Ethereum", "BTC", "gpumining", "EtherMining",\
           "Crypto_Currency_News", "CryptoCurrencyTrading", "ethtrader", "CryptoTechnology",\
            "BitcoinMarkets", "altcoin", "BinanceExchange", "ledgerwallet", "LitecoinMarkets",\
            "icocrypto", "BitcoinBeginners", "Dogecoin", "Monero", "Ripple", "RaiTrade", "xmrtrader" \
           ]

subreddit_string = ""
for i in sub_list:
  subreddit_string = subreddit_string +"+"+ str(i)
#print(subreddit_string)
iter_var = 0
#file_iter = 0
json_dict = {}
print ("Starting the stream.")
for submission in reddit.subreddit(subreddit_string).stream.submissions():
    try:
      json_dict[submission.id] = [submission.title, submission.score, submission.author.name]
    except:
      json_dict[submission.id] = [submission.title, submission.score, "Deleted"]
    
    if iter_var >= 100:
      print ("Writing to file.")
      try:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open('reddit_data/Reddit_data'+ timestr +'.json', 'w') as outfile:
          json.dump(json_dict, outfile)
        #file_iter = file_iter + 1
      except Exception as e:
        print (e.message)
        try:
          timestr = time.strftime("%Y%m%d-%H%M%S")
          with open('reddit_data/Reddit_data'+ timestr +'.json', 'w') as outfile:
            json.dump(json_dict, outfile)
          #file_iter = file_iter + 1
        except:
          print ("Failed writing to file again, moving on.")
        
        
      iter_var = 0
      json_dict = {}
      
    iter_var = iter_var + 1