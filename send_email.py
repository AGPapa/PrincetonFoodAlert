#Reads from stdin and sends emails
import smtplib
import sys

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

fromaddr = "ptonfoodalert@gmail.com"
pwd = "Enchilada333"

def send(netid, body):
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = netid + "@princeton.edu"
	msg['Subject'] = "Your Food Alert"

	msg.attach(MIMEText(body, 'html'))

	#sys.stderr.write(body)
	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, pwd)
	text = msg.as_string()
	server.sendmail(fromaddr,  netid + "@princeton.edu", text)
	server.quit()

	
get_netid = True
skip = False
lines = []
while True:
	s = sys.stdin.readline()
	if not s: break
	
	if (get_netid):
		netid = s[1:-2];
		get_netid = False
	elif (s == "<end of email>\n"):
		body = "".join(lines)
		send(netid, body)
		lines = []
		get_netid = True
	else:
		lines.append(s)