def true_round(number: float, length=0) -> float:
	# Получение цифр после запятой заданного числа
	digits = list(map(int, str(number).split('.')[1]))
    
	# Проход по цифрам в обратном порядке, начиная с той, которая находится на позиции length + 1
	for i in range(len(digits)-length, -1, -1):
		if digits[i] >= 5:
			digits[i-1] += 1
			digits[i] = 0
    
    # Если кол-во знаков после запятой (length) не было задано
	if length == 0:
		# Тогда округляем до целого числа (+1 к числу, если первая цифра после запятой >= 5)
		return float(str(number)[0]) + (1 if digits[0] >= 5 else 0)
	else:
		# Иначе формируем и возвращаем число с заданным кол-вом знаков после запятой
		return float(str(number)[0] + '.' + ''.join(map(str, digits[:length])))
