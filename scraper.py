from lxml import html
import requests
import codecs
import sys

butler_wilson = "02"
cjl = "05"
forbes = "03"
grad = "04"
rocky_mathey = "01"
whitman = "08"

def scrape(dhall_code):
	base_url = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?myaction=read'
	date= '&dtdate=4%2F7%2F2017'
	loc = '&locationNum=' + dhall_code
	page = requests.get(base_url + loc + date)
	
	tree = html.fromstring(page.content)
	breakfast = dinner = tree.xpath("//div[text()[contains(.,'Breakfast')]]/../../../../../..//a[@name='Recipe_Desc']/text()")
	lunch = dinner = tree.xpath("//div[text()[contains(.,'Lunch')]]/../../../../../..//a[@name='Recipe_Desc']/text()")
	dinner = tree.xpath("//div[text()[contains(.,'Dinner')]]/../../../../../..//a[@name='Recipe_Desc']/text()")
	print(breakfast)
	print()
	print(lunch)
	print()
	print(dinner)
	

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

scrape(whitman)