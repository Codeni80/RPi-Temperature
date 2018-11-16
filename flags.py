# def setFlags(temp0, temp1):
	# if temp0 > 75:
		# flag0 = True
	# else:
		# flag0 = False
	# if temp1 > 75:
		# flag1 = True
	# else:
		# flag1 = False
	# flags = []
	# flags.append(flag0)
	# flags.append(flag1)
	# return flags
	
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
		flag0 = "Probe 1 temperature is at optimal."
		
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
		flag1 = "Probe 2 temperature is at optimal."
		
	flags = []
	flags.append(flag0)
	flags.append(flag1)
	return flags