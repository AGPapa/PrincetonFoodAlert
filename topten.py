# Iterates through food preferences database and creates a list of the
# top ten current most popular foods. Then creates a entry in the 
# Top_Ten collection for that date and the current top ten foods. Html
# code can then pull from that collection for display on the web page.

import os
import sys
import pymongo
import datetime

uri = 'mongodb://foodpref:hungry67@ds153730.mlab.com:53730/heroku_b3r535zh'

# code from foodalert.py
# Connects to database and Users collection
client = None
db = None
users = None
try:
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    users = db.get_collection("Users")
except Exception as e:
    print(str(e))


# Creates dictionary for foods and their preference numbers
prefs = {}

# Populates prefs dictionary based on current database
all = users.find()
for usr in all:

	try:

		for food in usr["foodpref"]:
			if food.lower() in prefs:
				prefs[food.lower()] += 1
			else:
				prefs[food.lower()] = 1
	except KeyError:
		pass
		
# Sorts keys and obtains top ten most popular foods
recent = sorted(prefs, key=prefs.get, reverse=True)[:10]
# print recent

# Accesses Top_Ten collection
try:
	topten = db.get_collection("Top_Ten")
except Exception as e:
    print(str(e))

full_date = datetime.datetime.utcnow()
date = full_date.strftime("%Y-%m-%d")
# print date

# Adds new entry in Top_Ten for that date and the current top ten
topten.update_one({'date':date}, {'$set' : {'topten':recent}}, upsert=True)



