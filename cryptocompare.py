# Gets the historical 1min data starting from 6 days before to now
import requests
import datetime
import time as t
import json
from dotenv import load_dotenv, find_dotenv
import os
symbols = ['BTC', 'XRP', 'ETH', 'XLM', 'BCH', 'EOS', 'BSV', 'LTC', 'TRX', 'ADA', 'XMR', 'BNB', 'XEM', 'IOT',
           'DASH', 'ETC', 'NEO', 'ZEC', 'DOGE']  # Top 20 Coins
time = datetime.datetime.utcnow()  # GMT 0 Current Time
now = datetime.datetime.utcnow()
dt = datetime.timedelta(days=6)
time -= dt
if not os.path.exists('cryptocompare_data'):
	os.makedirs('cryptocompare_data')
load_dotenv(find_dotenv())
key = os.environ.get('CRYPTOCOMPARE_KEY')
def collect(customTime, array, currentTime):
    while customTime <= currentTime:
        for element in array:
            response = requests.get(
                'https://min-api.cryptocompare.com/data/histominute?'
                'fsym=%s&tsym=USD&limit=1&toTs=%d'
                '&api_key=%s'
                % (element, customTime.timestamp(), key))
            t.sleep(1)
            if response.status_code == 200:  # Request is successful
                print("STATUS CODE 200")
                data = response.json()['Data']
                print (data)
                with open(f"cryptocompare_data/{element}_{customTime.strftime('%d%m%Y-%H%M%S')}.json", 'w') as outfile:
                    json.dump(data,outfile)
            elif response.status_code == 429:
                print("STATUS CODE 429")
                t.sleep(600)
                collect(customTime, [element], customTime + 60)
            else:
                collect(customTime, [element], customTime + 60)
        currentTime = datetime.datetime.utcnow()
        customTime += datetime.timedelta(minutes=2)
    if customTime > currentTime:
        return customTime, currentTime


while True:
    if time <= now:
        try:
            time, now = collect(time, symbols, now)
        except:
            t.sleep(600)
    else:
        t.sleep(120)
        now = datetime.datetime.utcnow()
