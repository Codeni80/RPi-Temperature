import sys, time, rrdtool, shutil, re, os
import RPi.GPIO as GPIO
import flags, graphing

temp1 = 0
temp0 = 0
attempts = 0

while (attempts < 5):
	#Sensor locations
	temp2Store = open("/sys/bus/w1/devices/28-000005cfd62d/w1_slave")
	temp1Store = open("/sys/bus/w1/devices/28-000005cfd13f/w1_slave")
	#Read in information about first sensor & close sensor
	data1 = temp1Store.read()
	
	#Format information from above to be usable
	temp1Data = data1.split("\n")[1].split(" ")[9]
	temp1 = float(temp1Data[2:])
	temp1 = temp1/1000 #C
	temp1 = temp1 * (9/5) + 32 #F


	#Read information about first sensor & close sensor
	data2 = temp2Store.read()

	#Format information from above to be usable
	temp2Data = data2.split("\n")[1].split(" ")[9]
	temp2 = float(temp2Data[2:])
	temp2 = temp2/1000 #C
	temp2 = temp2 * (9/5) + 32 #F
	
	#Formatting temperature to an easier to read form 
	temp1 = '{0:.6g}'.format(temp1)
	temp2 = '{0:.6g}'.format(temp2)

	#Create update to temperature.rrd in order to add our newly read information.
	ret = rrdtool.update('temperature.rrd',"N:{0}:{1}".format(temp1, temp2))
	print(rrdtool.lastupdate("temperature.rrd"))
	result = rrdtool.lastupdate("temperature.rrd")
	
	#Pulling the latest time, and temps from the rrd file
	time = result['date']
	temp0 = result['ds']['temp0']
	temp1 = result['ds']['temp1']

	#Making sure to close the open sensor location files
	temp1Store.close()
	temp2Store.close()
	attempts += 1

#Call to alertCheck to check for abnormal temperatures and to create graphs of the data.
graphing.alertCheck(temp0, temp1, time)

#Copying locally created graphs to the /var/www/html folder to be displayed on the webpage
graphing.copyGraph()
