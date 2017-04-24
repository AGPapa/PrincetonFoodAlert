import sys

def write_email(netid, foodprefs, dhalls, dates, meals, foods):
	sys.stdout.write("\n<email for " + netid + ">\n")
	count = 0
	for food in foodprefs:
		count = count + 1
	sys.stdout.write("Hello " + netid + ", you have " + str(count) + " food(s) in the dining halls in the next week." + "\n")
	for i in range(0, count):
		sys.stdout.write("On " + dates[i] + " there will be " + foods[i][:-1] + " in " + dhalls[i] + " for " + meals[i] + ". You recieved this notification because you wanted emails for \"" + foodprefs[i] + "\".\n")
	sys.stdout.write("Thank you for using Princeton Food Alert. Please visit www.ptonfoodalert.herokuapp.com to update your preferences.\n")
	sys.stdout.write("<end email>\n")


foodprefs = []
dhalls = []
dates = []
meals = []
foods = []

first_line = sys.stdin.readline()
tokens = first_line.split("\t")
netid = tokens[0];
foodprefs.append(tokens[1])
dhalls.append(tokens[2])
dates.append(tokens[3])
meals.append(tokens[4])
foods.append(tokens[5])
while True:
	s = sys.stdin.readline()
	if not s: break
	
	tokens = s.split("\t")
	if (netid == tokens[0]):
		foodprefs.append(tokens[1])
		dhalls.append(tokens[2])
		dates.append(tokens[3])
		meals.append(tokens[4])
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
		dhalls.append(tokens[2])
		dates.append(tokens[3])
		meals.append(tokens[4])
		foods.append(tokens[5])
