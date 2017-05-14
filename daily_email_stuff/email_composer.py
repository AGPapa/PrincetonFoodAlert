import sys
import datetime
import pymongo

DayL = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
MonthL = [' ', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def write_email(netid, foodprefs, dhalls, dates, meals, foods, netids):

	try:
		name = netids[netid]
	except:
		name = netid

	sys.stdout.write("<" + netid + ">\n")
	count = 0
	for food in foodprefs:
		count = count + 1
	sys.stdout.write("<p>Hello " + name + ", you have " + str(count) + " food(s) in the dining halls in the next week.</p>")
	sys.stdout.write("""
<head>
	<style>
		table, th, td {
			border: 1px solid black;
		}
	</style>
</head>
<table>
	<tr>
		<th>Date</th>
		<th>Dining Hall</th>
		<th>Food in Dining Hall</th>
		<th>Matched with</th>
	</tr>""")
	for i in range(0, count):
		month = int(dates[i][:2])
		day = int(dates[i][3:])
		day_of_week = DayL[datetime.date(2017,month,day).weekday()]
#		sys.stdout.write("There will be " + foods[i][:-1] + " in " + dhalls[i] + " for " + meals[i] + " on " + day_of_week + ", " + MonthL[month] + " " + str(day) + ". You received this notification because you wanted emails for \"" + foodprefs[i] + "\".\n")
		sys.stdout.write("""
	<tr>
		<td>""" + meals[i] + ", " + day_of_week + ", " + MonthL[month] + " " + str(day) + """</td>
		<td>""" + dhalls[i] + """</td>
		<td>""" + foods[i][:-1] + """</td>
		<td>""" + foodprefs[i] + """</td>
	</tr>""")
	sys.stdout.write("\n</table>")
	sys.stdout.write("\n<p>Thank you for using Princeton Food Alert. Please visit ptonfoodalert.herokuapp.com if you wish to update your preferences.</p>\n")
	sys.stdout.write("<end of email>\n")



uri = 'mongodb://foodpref:hungry67@ds153730.mlab.com:53730/heroku_b3r535zh'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
all = db.get_collection("NetIDs").find()
netids = all[0]

foodprefs = []
dhalls = []
dates = []
meals = []
foods = []

first_line = sys.stdin.readline()
tokens = first_line.split("\t")
netid = tokens[0];
foodprefs.append(tokens[1])
dates.append(tokens[2])
meals.append(tokens[3])
dhalls.append(tokens[4])
foods.append(tokens[5])
while True:
	s = sys.stdin.readline()
	if not s: break
	
	tokens = s.split("\t")
	if (netid == tokens[0]):
		foodprefs.append(tokens[1])
		dates.append(tokens[2])
		meals.append(tokens[3])
		dhalls.append(tokens[4])
		foods.append(tokens[5])
	else:
		write_email(netid, foodprefs, dhalls, dates, meals, foods, netids)
		
		#clear old data
		foodprefs = []
		dhalls = []
		dates = []
		meals = []
		foods = []
		
		#enter new data
		netid = tokens[0];
		foodprefs.append(tokens[1])
		dates.append(tokens[2])
		meals.append(tokens[3])
		dhalls.append(tokens[4])
		foods.append(tokens[5])
