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
	
	tempComment = "Probe 1 temperature is - {0}  Probe 2 temperature is - {1}".format(temp0, temp1)
	#Opening log file
	f = open("log/temp.log", "a")
	#All f.writes are written to the log file to help us ensure that we have backup copies of our temperature
	#data to allow us to access recorded temperatures if something happens to our graphs, or to check for excessive
	#lengths of high temperatures if they are far enough in the past to no longer be shown on the graph itself
	#(basically the log file is for historical data)
	f.write("Date/Time of run: {0}\n".format(time))
	f.write(tempComment)
	createGraph(flag0, flag1, tempComment)
	f.close()
		
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
						"COMMENT: {0}".format(tempComment))

	#Daily Graph
	ret = rrdtool.graph("temp_daily.png", "--start", "-1d", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [deg F]".format(INTEMP_COLOR))
						
	#Weekly Graph
	ret = rrdtool.graph("temp_weekly.png", "--start", "-1w", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [deg F]".format(INTEMP_COLOR))
						
	#Monthly Graph
	ret = rrdtool.graph("temp_monthly.png", "--start", "-1m", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [deg F]".format(INTEMP_COLOR))
						
	#Yearly Graph
	ret = rrdtool.graph("temp_yearly.png", "--start", "-1yh", "--vertical-label=Degrees F",
						"DEF:temp0=temperature.rrd:temp0:AVERAGE",
						"LINE2:temp0{0}:Probe 1 [deg F]".format(OUTTEMP_COLOR),
						"DEF:temp1=temperature.rrd:temp1:AVERAGE",
						"LINE2:temp1{0}:Probe 2 [deg F]".format(INTEMP_COLOR))
						
def copyGraph():
	#Send a copy of the graphs to /var/www/html/ to be displayed on the webpage
	shutil.copy2('/home/pi/test-stuff/python/temp_hourly.png', '/var/www/html/temp_hourly1.png')
	shutil.copy2('/home/pi/test-stuff/python/temp_daily.png', '/var/www/html/temp_daily1.png')
	shutil.copy2('/home/pi/test-stuff/python/temp_weekly.png', '/var/www/html/temp_weekly1.png')
	shutil.copy2('/home/pi/test-stuff/python/temp_monthly.png', '/var/www/html/temp_monthly1.png')
	shutil.copy2('/home/pi/test-stuff/python/temp_yearly.png', '/var/www/html/temp_yearly1.png')