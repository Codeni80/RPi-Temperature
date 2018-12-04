import requests, time
from datetime import datetime

def send_sms(temps):
	report = {}
	report["value1"] = temps[0]
	report["value2"] = temps[1]
	requests.post("https://maker.ifttt.com/trigger/SendMessage/with/key/<key removed for github>", data=report)
	
def format_sms(temp0, temp1):
	temp0 = '{0:.4g}'.format(temp0)
	temp1 = '{0:.4g}'.format(temp1)
	temps = []
	temps.append(temp0)
	temps.append(temp1)
	return(temps)
	
def log_sms(time):
	f = open("log/lastsms.log", "w")
	f.write(str(time))
	f.close()

def check_sms_log(time):
	f = open("log/lastsms.log", "r")
	logTime = f.read()
	f.close()
	logTime = logTime.strip("\n")
	try:
		logTime = datetime.strptime(logTime, "%Y-%m-%d %H:%M:%S")
		smsCheck = time - logTime
		hours = smsCheck.seconds//3600
		days = smsCheck.days
		smsCheck = hours + (days*24)
		return(smsCheck)
	except ValueError:
		return(1)