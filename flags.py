import rrdtool
	
def setFlags(temp0, temp1):
	if temp0 > 70 and temp0 < 75:
		#Temp0 is safe, but slightly high
		flag0 = "Probe 1 temperature is safe, but higher than ideal."
	elif temp0 >= 75 and temp0 < 80:
		#Temp0 is to high
		flag0 = "Probe 1 temperature is high."
	elif temp0 >= 80:
		#Temp0 is dangerously high
		flag0 = "Probe 1 temperature is dangerously high!" 
	else:
		#Temp0 is good
		flag0 = "Probe 1 temperature is optimal."
		
	if temp1 > 70 and temp1 < 75:
		#Temp1 is safe, but slightly high
		flag1 = "Probe 2 temperature is safe, but higher than ideal."
	elif temp1 >= 75 and temp1 < 80:
		#Temp1 is to high
		flag1 = "Probe 2 temperature is high."
	elif temp1 >= 80:
		#Temp1 is dangerously high
		flag1 = "Probe 2 temperature is dangerously high!"
	else:
		#Temp1 is good
		flag1 = "Probe 2 temperature is optimal."
		
	flags = []
	flags.append(flag0)
	flags.append(flag1)
	return flags
	
def average(time):
	if time == 0:
		#Hourly
		start = "-1h"
	elif time == 1:
		#Daily
		start = "-1d"
	elif time == 2:
		#Weekly
		start = "-1w"
	elif time == 3:
		#Monthly
		start = "-1m"
	elif time == 4:
		#Yearly
		start = "-1y"
	else:
		#Error
		return("Error - time was not sent properly")
	temps = rrdtool.fetch("temperature.rrd", "--start={0}".format(start), "AVERAGE")
	rows = temps[2]
	count = 0
	total = 0
	total2 = 0
	for item in rows:
		if item[0] is not None:
			total += item[0]
			count += 1
		if item[1] is not None:
			total2 += item[1]
	average1 = total / count
	average1 = '{0:.6g}'.format(average1)
	average2 = total2 / count
	average2 = '{0:.6g}'.format(average2)
	average = "Probe 1\: {0} Probe 2\: {1}".format(average1, average2)
	return(average)