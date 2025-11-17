def normal_round(number, length=0):
	try:
		result = [int(i) for i in (str(number).split('.')[1])][::-1]
		for i in range(0, len(result)-length-1):
			if result[i] >= 5:
				result[i+1] += 1
				result[i] = 0
		sec_number = [str(number).split('.')[0], ("".join([str(i) for i in result[::-1]]))]
		if length == 0:
			if int(sec_number[1][0]) >= 5:
				return (int(sec_number[0])+1)
			else: return int(sec_number[0])
		else: return float(sec_number[0]+'.'+sec_number[1][0:length])
	except: return number
