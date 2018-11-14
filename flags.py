def setFlags(temp0, temp1):
	if temp0 > 80:
		flag0 = True
	else:
		flag0 = False
	if temp1 > 80:
		flag1 = True
	else:
		flag1 = False
	flags = []
	flags.append(flag0)
	flags.append(flag1)
	return flags