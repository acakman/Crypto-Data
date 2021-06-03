import python_forex_quotes
import time
import json
import os
import sys
from dotenv import load_dotenv, find_dotenv
#You can get an API key for free at 1forge.com
load_dotenv(find_dotenv())
key = os.environ.get("FOREX_KEY")

if not os.path.exists('forex_data'):
	os.makedirs('forex_data')


key_num = 0
query_count = 1
client = python_forex_quotes.ForexDataClient(key)
symbol_list = client.getSymbols()#will be read from the database

quota = client.quota()
if quota['error'] == True:
  print("Invalid key, exiting...")
  sys.exit(0)
print(quota)
hours_until_refresh = quota['hours_until_reset']
quota_rem = quota['quota_remaining']
print ("Quota remaining: " + str(quota_rem))

if quota_rem == 0: #check whether there is remaining qouta, if not sleep 
  print ("No quota remaining, sleeping until refresh.")
  time.sleep(hours_until_refresh*60*60)
  print ("Woke up")

file_iter = 1
the_list = []
sleep_iter = 0
while True: #query_count <= 10:#delete for success
      try:
        the_list.append(client.getQuotes(symbol_list))
      except:
        print ("Couldnt get symbol list")
        continue
      print ("Waiting one minute. " + str(sleep_iter))
      time.sleep(58)
      sleep_iter = sleep_iter + 1
      quota_rem = quota_rem-1
      print (quota_rem)
      #if quota_rem <= 0: #if we have no quota left sleep
      if sleep_iter % 50 == 0:
        print ("No quota remaining")
        try:#write to file.
          timestr = time.strftime("%Y%m%d-%H%M%S")
          
          with open('forex_data/forex_data_' + timestr + '.json', 'w') as outfile:
            query_count = query_count + 1
            json.dump(the_list, outfile)
            file_iter = file_iter + 1
            the_list = []
            print ("Written to file.")
            sleep_iter = 0
        except:
          print ("Problem writing to file.")
      if quota_rem <= 0: #if we have no quota left sleep
        print ("Time to sleep...")
        quota = client.quota()#get new quota to learn how much we should sleep.
        hours_until_refresh = quota['hours_until_reset']
        quota_rem = quota['quota_remaining']
        print ("Quota remaining: " + str(quota_rem))
        print ("sleeping for " + str(hours_until_refresh*60*60) + " hours")
        time.sleep(hours_until_refresh*60*60)#sleep until refresh
        print ("Good Morning")
        quota = client.quota()
        hours_until_refresh = quota['hours_until_reset']
        quota_rem = quota['quota_remaining']
        print ("I have " + str(quota_rem) + " quota remaining!")
        while quota_rem == 0: #if quota has not been refreshed yet sleep and check again until it is.
          print ("Sleeping again...")
          time.sleep(hours_until_refresh*60*60)
          quota = client.quota()
          hours_until_refresh = quota['hours_until_reset']
          quota_rem = quota['quota_remaining']