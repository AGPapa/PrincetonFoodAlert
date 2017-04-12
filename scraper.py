from lxml import html
from unidecode import unidecode
import requests
import codecs
import sys

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
	

#UTF8Writer = codecs.getwriter('utf8')
#sys.stdout = UTF8Writer(sys.stdout)

dhalls = {'butler_wilson' : "02", 'cjl' : "05", 'forbes' : "03", 'grad' : "04", 'rocky_mathey' : "01", 'whitman' : "08"}
for day in range (11, 19):
	for key in dhalls:
		(b, l, d) = scrape(dhalls.get(key), "4", str(day).zfill(2))
		for food in b:
			print(key + "\t" + "04-" + str(day).zfill(2) + "\t" + "breakfast" + "\t" + unidecode(food))
		for food in l:
			print(key + "\t" + "04-" + str(day).zfill(2) + "\t" + "lunch" + "\t" + unidecode(food))
		for food in d:
			print(key + "\t" + "04-" + str(day).zfill(2) + "\t" + "dinner" + "\t" + unidecode(food))