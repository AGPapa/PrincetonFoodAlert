# scrapes the dining hall website, outputting the food options for each dining hall for each day and meal

from lxml import html
from unidecode import unidecode
import requests
import codecs
import sys
import datetime

butler_wilson = "02"
cjl = "05"
forbes = "03"
grad = "04"
rocky_mathey = "01"
whitman = "08"

def scrape(dhall_code, month, day):
	base_url = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?myaction=read'
	date= '&dtdate=' + month + '%2F' + day + '%2F2017'
	loc = '&locationNum=' + dhall_code
	page = requests.get(base_url + loc + date)
	
	tree = html.fromstring(page.content)
	breakfast  = tree.xpath("//div[text()[contains(.,'Breakfast')]]/../../../../../..//a[@name='Recipe_Desc']/text()")
	lunch = tree.xpath("//div[text()[contains(.,'Lunch')]]/../../../../../..//a[@name='Recipe_Desc']/text()")
	dinner = tree.xpath("//div[text()[contains(.,'Dinner')]]/../../../../../..//a[@name='Recipe_Desc']/text()")
	return (breakfast, lunch, dinner)
	



dhalls = {'Butler/Wilson' : "02", 'the Center For Jewish Life' : "05", 'Forbes' : "03", 'the Graduate College' : "04", 'Rocky/Mathey' : "01", 'Whitman' : "08"}
now = datetime.datetime.now();	
for i in range (0, 8):
	day = now.day
	month = now.month
	now += (datetime.timedelta(days=1))
	
	for key in dhalls:
		(b, l, d) = scrape(dhalls.get(key), str(month), str(day).zfill(2))
		for food in b:
			print(str(month).zfill(2) + "-" + str(day).zfill(2) + "\t" + "Breakfast" + "\t" + key + "\t" + unidecode(food))
		for food in l:
			print(str(month).zfill(2) + "-" + str(day).zfill(2) + "\t" + "Lunch" + "\t" + key + "\t" + unidecode(food))
		for food in d:
			print(str(month).zfill(2) + "-" + str(day).zfill(2) + "\t" + "Dinner" + "\t" + key + "\t" + unidecode(food))