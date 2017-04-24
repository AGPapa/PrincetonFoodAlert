# Import smtplib for the actual sending function
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def check_dhall(food_item):
	return True

def get_likers(food_item):
	return ["mhammel@princeton.edu", "thclark@princeton.edu", "ra4@princeton.edu", "agpapa@princeton.edu"]
	#return ["joseip@princeton.edu", "jdbrooks@princeton.edu", "ngadiano@princeton.edu", "migoe@princeton.edu"]

def get_today_menu():
	return ["Enchiladas", "Rigatoni la Nonna"]

fromaddr = "email@address.com"
pwd = "password"

for food_name in get_today_menu():
	recipients = get_likers(food_name)
	msg = MIMEMultipart()
	dhall_name = "Rocky-Mathey"
	msg['From'] = fromaddr
	msg['To'] = ", ".join(recipients)
	msg['Subject'] = "%s in %s" % (food_name, dhall_name)

	body = "Your favorite food, %s, is being served in the %s Dining Halls" % (food_name, dhall_name)
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, pwd)
	text = msg.as_string()
	server.sendmail(fromaddr, recipients, text)
	server.quit()
