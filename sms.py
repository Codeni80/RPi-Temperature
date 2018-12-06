import requests, time
from datetime import datetime

#Using IFTTT webhook to send push notifications to device
def send_sms(temps):
	report = {}
	report["value1"] = temps[0]
	report["value2"] = temps[1]
	requests.post("https://maker.ifttt.com/trigger/PushNotif/with/key/<Removed>", data=report)

def file_error_sms(type):
	if(type == 1):
		#Write error
		requests.post("https://maker.ifttt.com/trigger/OpenWError/with/key/A-bZYXN4teHcgT7H_vWYj")
	elif(type == 2):
		#Read error
		requests.post("https://maker.ifttt.com/trigger/OpenRError/with/key/A-bZYXN4teHcgT7H_vWYj")
	elif(type == 3):
		#Temperature log error
		requests.post("https://maker.ifttt.com/trigger/OrigLogError/with/key/A-bZYXN4teHcgT7H_vWYj")
	else:
		#Ivalid Data Passed
		requests.post("https://maker.ifttt.com/trigger/AccessError/with/key/A-bZYXN4teHcgT7H_vWYj", data = type)

#Formating the SMS to be shorter and easier to read at a glance on the device.
def format_sms(temp0, temp1):
	temp0 = '{0:.4g}'.format(temp0)
	temp1 = '{0:.4g}'.format(temp1)
	temps = []
	temps.append(temp0)
	temps.append(temp1)
	return(temps)
	
#Using a logging file in order to track when the last SMS was sent.
#This is useful to avoid spamming SMSs to users.
def log_sms(time):
	try:
		f = open("log/lastsms.log", "w")
		f.write(str(time))
		f.close()
	except IOError:
		print("Could not open log file to write.")
		file_error_sms(1)

#Checking the SMS log file to see when the last SMS sent was, and to take appropriate action based on length
#of time since the lase SMS was sent.
def check_sms_log(time):
	try:
		f = open("log/lastsms.log", "r")
		logTime = f.read()
		f.close()
		logTime = logTime.strip("\n")
		#Trying to convert the data from log file to datetime format
		try:
			logTime = datetime.strptime(logTime, "%Y-%m-%d %H:%M:%S")
			smsCheck = time - logTime
			hours = smsCheck.seconds//3600
			days = smsCheck.days
			smsCheck = hours + (days*24)
			return(smsCheck)
		#If data is invalid from the log file, we simply send a signal of 1 to allow an SMS to be sent
		#This will also allow us to fix whatever issue arose in the log file by overwritting it with a valid
		#datetime stamp
		except ValueError:
			return(1)
	except IOError:
		print("Could not open log file to read.")
		file_error_sms(2)
