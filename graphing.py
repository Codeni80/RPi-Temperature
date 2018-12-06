import rrdtool
import shutil, re, os
import flags, sms


INTEMP_COLOR = "#CC0000"
OUTTEMP_COLOR = "#0000FF"

def alertCheck(temp0, temp1, time):
	#Call to setFlags to check for abnormal temperatures
	result = flags.setFlags(temp0, temp1)
	flag0 = result[0]
	flag1 = result[1]
	
	tempComment = "Probe 1 temperature is - {0}  Probe 2 temperature is - {1}".format(temp0, temp1)
	#Opening log file
	try:
		f = open("log/temp.log", "a")
		#All f.writes are written to the log file to help us ensure that we have backup copies of our temperature
		#data to allow us to access recorded temperatures if something happens to our graphs, or to check for excessive
		#lengths of high temperatures if they are far enough in the past to no longer be shown on the graph itself
		#(basically the log file is for historical data)
		f.write("Date/Time of run: {0}\n".format(time))
		f.write(tempComment)
		f.write("\n")
		createGraph(flag0, flag1, tempComment)
		f.close()
	except IOError:
		sms.file_error_sms(3)
		
def createGraph(p1Comment, p2Comment, tempComment):
	#Hourly Graph
	ret = rrdtool.graph("temp_hourly.png", "--start"," -4h", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [deg F]".format(INTEMP_COLOR),
						"COMMENT:  ",
						"COMMENT: {0}".format(p1Comment),
						"COMMENT: {0}".format(p2Comment),
						"COMMENT: {0}".format(tempComment),
						"COMMENT: Hourly Average Temperatures - {0}".format(flags.average(0)))

	#Daily Graph
	ret = rrdtool.graph("temp_daily.png", "--start", "-1d", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [deg F]".format(INTEMP_COLOR),
						"COMMENT: Daily Average Temeratures - {0}".format(flags.average(1)))
						
	#Weekly Graph
	ret = rrdtool.graph("temp_weekly.png", "--start", "-1w", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [deg F]".format(INTEMP_COLOR),
						"COMMENT: Weekly Average Temperatures - {0}".format(flags.average(2)))
						
	#Monthly Graph
	ret = rrdtool.graph("temp_monthly.png", "--start", "-1m", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [deg F]".format(INTEMP_COLOR),
						"COMMENT: Monthly Average Temperatures - {0}".format(flags.average(3)))
						
	#Yearly Graph
	ret = rrdtool.graph("temp_yearly.png", "--start", "-1y", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [deg F]".format(INTEMP_COLOR),
						"COMMENT: Yearly Average Temperatures - {0}".format(flags.average(4)))
						
def copyGraph():
	#Send a copy of the graphs to /var/www/html/ to be displayed on the webpage
	shutil.copy2('/home/pi/pitemp/temp_hourly.png', '/var/www/html/temp_hourly1.png')
	shutil.copy2('/home/pi/pitemp/temp_daily.png', '/var/www/html/temp_daily1.png')
	shutil.copy2('/home/pi/pitemp/temp_weekly.png', '/var/www/html/temp_weekly1.png')
	shutil.copy2('/home/pi/pitemp/temp_monthly.png', '/var/www/html/temp_monthly1.png')
	shutil.copy2('/home/pi/pitemp/temp_yearly.png', '/var/www/html/temp_yearly1.png')