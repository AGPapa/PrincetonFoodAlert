import sys
import datetime

DayL = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
MonthL = [' ', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def write_email(netid, foodprefs, dhalls, dates, meals, foods):
	
	sys.stdout.write("<" + netid + ">\n")
	count = 0
	for food in foodprefs:
		count = count + 1
	sys.stdout.write("<p>Hello " + netid + ", you have " + str(count) + " food(s) in the dining halls in the next week.</p>")
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
		write_email(netid, foodprefs, dhalls, dates, meals, foods)
		
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
