import rrdtool
import shutil, re, os
import flags


INTEMP_COLOR = "#CC0000"
OUTTEMP_COLOR = "#0000FF"

def alertCheck(temp0, temp1, time):
	#Call to setFlags to check for abnormal temperatures
	result = flags.setFlags(temp0, temp1)
	flag0 = result[0]
	flag1 = result[1]
	f = open("log/temp.log", "a")
	f.write("Date/Time of run: {0}\n".format(time))
	if flag0 == True and flag1 == True:
		#Both temps are too high
		f.write("******ALERT******\n")
		f.write("Temp0: {0} \t Temp1: {1}\n".format(temp0, temp1))
		alertComment = "*****ALERT*****"
		messageComment = "Both probes temperatures are too high!"
		tempComment = "Probe 1 - {0}\tProbe 2 - {1}".format(temp0, temp1)
		createGraph(alertComment, messageComment, tempComment)
	elif flag0 == False and flag1 == False:
		#Both temps are good temperature
		f.write("Temp0: {0} \t Temp1: {1}\n".format(temp0, temp1))
		alertComment = "   "
		messageComment = "Both probes are at a safe temperature"
		tempComment = "Probe 1 - {0}\tProbe 2 - {1}".format(temp0, temp1)
		createGraph(alertComment, messageComment, tempComment)
	elif flag0 == True and flag1 == False:
		#Temp0 is too high, Temp1 is fine.
		f.write("***ALERT*** Temp0: {0} \t Temp1: {1}\n".format(temp0, temp1))
		alertComment = "***ALERT***"
		messageComment = "Probe 1 temperature is too high!"
		tempComment = "Probe 1 - {0}\tProbe 2 - {1}".format(temp0, temp1)
		createGraph(alertComment, messageComment, tempComment)
	elif flag0 == False and flag1 == True:
		#Temp1 is too high, Temp0 is fine.
		f.write("Temp0: {0} \t ***ALERT*** Temp1: {1}\n".format(temp0, temp1))
		alertComment = "***ALERT***"
		messageComment = "Probe 2 temperature is too high!"
		tempComment = "Probe 1 - {0}\tProbe 2 - {1}".format(temp0, temp1)
		createGraph(alertComment, messageComment, tempComment)
	#Closing log file
	f.close()
		
def createGraph(alertComment, messageComment, tempComment):
	#Hourly Graph
	ret = rrdtool.graph("temp_hourly.png", "--start"," -4h", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [def F]".format(INTEMP_COLOR),
						"COMMENT:  ",
						"COMMENT: {0}".format(alertComment),
						"COMMENT: {0}".format(messageComment),
						"COMMENT: {0}".format(tempComment))

	#Daily Graph
	ret = rrdtool.graph("temp_daily.png", "--start", "-1d", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [def F]".format(INTEMP_COLOR))
						
	#Weekly Graph
	ret = rrdtool.graph("temp_weekly.png", "--start", "-1w", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [def F]".format(INTEMP_COLOR))
						
	#Monthly Graph
	ret = rrdtool.graph("temp_monthly.png", "--start", "-1m", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [def F]".format(INTEMP_COLOR))
						
	#Yearly Graph
	ret = rrdtool.graph("temp_yearly.png", "--start", "-1yh", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [def F]".format(INTEMP_COLOR))
						
def copyGraph():
	#Send a copy of the graphs to /var/www/html/ to be displayed on the webpage
	shutil.copy2('/home/pi/test-stuff/python/temp_hourly.png', '/var/www/html/temp_hourly1.png')
	shutil.copy2('/home/pi/test-stuff/python/temp_daily.png', '/var/www/html/temp_daily1.png')
	shutil.copy2('/home/pi/test-stuff/python/temp_weekly.png', '/var/www/html/temp_weekly1.png')
	shutil.copy2('/home/pi/test-stuff/python/temp_monthly.png', '/var/www/html/temp_monthly1.png')
	shutil.copy2('/home/pi/test-stuff/python/temp_yearly.png', '/var/www/html/temp_yearly1.png')