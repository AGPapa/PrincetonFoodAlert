# reads in dhall options and matches with users
import sys
import pymongo
import json
import datetime

def check_date(dhall_line):
	tokens = dhall_line.split('\t')
	
	now = datetime.datetime.now();
	dateText = tokens[0]
	date = datetime.datetime(now.year, int(dateText[:2]), int(dateText[3:]), now.hour, now.minute, 0)
	delta = date - now;
	return (delta.days == -1 or delta.days == 5) #off by one, idk

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
		if (check_date(s)):
			for food in user['foodpref']:
				if match(food.lower(), s):
					sys.stdout.write(user['netid'] +  "\t" + food + "\t" + s)
	all.rewind()