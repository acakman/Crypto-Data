import requests
import json
import time
import os

if not os.path.exists('what_to_mine_data'):
	os.makedirs('what_to_mine_data')

while True:
	try:
		response = requests.get("https://whattomine.com/coins.json")
		if response.status_code == 200:
			data = response.json()
	except Exception as e: 
		print(e)
	timestr = time.strftime("%Y%m%d-%H%M%S")
	try:
		with open('what_to_mine_data/what_to_mine_' + timestr + '.json', 'w') as outfile:
			json.dump(data, outfile)
	except:
		print("Problem writing to file, trying again.")
		try:
			with open('what_to_mine_data/what_to_mine_' + timestr + '.json', 'w') as outfile:
					json.dump(data, outfile)
		except:
			print("Failed second write attempt, moving onto next json")
	time.sleep(300)
	
