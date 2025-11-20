def normal_round(number, length=0) -> float:
	digits = [int(i) for i in (str(number).split('.')[1])][::-1]
	for i in range(0, len(digits)-length-1):
		if digits[i] >= 5:
			digits[i+1] += 1
			digits[i] = 0
	sec_number = [str(number).split('.')[0], ("".join([str(i) for i in digits[::-1]]))]
	if length == 0:
		if int(sec_number[1][0]) >= 5:
			return (int(sec_number[0])+1)
		else: return int(sec_number[0])
	else: return float(sec_number[0]+'.'+sec_number[1][0:length])
