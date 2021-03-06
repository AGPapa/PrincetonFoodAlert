# reads in dhall options and matches with users
import sys
import pymongo
import json
import datetime
import time

def check_date(dhall_line, day_before, week_before, dhall_pref):
	tokens = dhall_line.split('\t')
	
	if ('b' not in dhall_pref and tokens[2] == "Butler/Wilson"):
		return False
	elif ('r' not in dhall_pref and tokens[2] == "Rocky/Mathey"):
		return False
	elif ('f' not in dhall_pref and tokens[2] == "Forbes"):
		return False
	elif ('w' not in dhall_pref and tokens[2] == "Whitman"):
		return False
	elif ('c' not in dhall_pref and tokens[2] == "the Center For Jewish Life"):
		return False
	elif ('g' not in dhall_pref and tokens[2] == "the Graduate College"):
		return False

	now = datetime.datetime.now();
	dateText = tokens[0]
	date = datetime.datetime(now.year, int(dateText[:2]), int(dateText[3:]), now.hour, now.minute, 0)
	delta = date - now;
	return ((day_before and delta.days == -1) or (week_before and delta.days == 5)) #off by one, idk

def match(food, dhall_line):
	tokens = dhall_line.split('\t')
	
	wordsDhall = tokens[3].lower().strip().split(' ')
	wordsFood = food.split(' ')
	match = 0
	count = 0
	for wordFood in wordsFood:
		count = count + 1
		for wordDhall in wordsDhall:
			if wordFood == wordDhall:
				match = match + 1
				break
				
	return (match == count)


uri = 'mongodb://foodpref:hungry67@ds153730.mlab.com:53730/heroku_b3r535zh'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
users = db.get_collection("Users")
all = users.find()

while True:
	s = sys.stdin.readline()
	if not s: break
	for user in all:
		start = time.time();
		try:
			day_before = 'd' in user['accountpref']
			week_before = 'w' in user['accountpref']
		except:
			day_before = True
			week_before = True
		try:
			dhall_pref = user['dhallpref']
		except:
			dhall_pref = 'brfwcg'
		try:	
			if (check_date(s, day_before, week_before, dhall_pref)):
				for food in user['foodpref']:
					if match(food.lower(), s):
						sys.stdout.write(user['netid'] +  "\t" + food + "\t" + s)
		except KeyError:
			pass
	all.rewind()