from .custom_round import true_round
from time import sleep, time_ns


class PseudoRandom:
	@staticmethod
	def get_random_number(length=1) -> int:
		""" Генерация псевдослучайного числа заданной длины """
		number = ''
		while len(number) != length:
            # Генерация псевдослучайной цифры на основе текущего времени и "волшебных" математических операций
			number += str(int(((int(str(int((time_ns()*1.71)/0.8))[::-1])**0.5)*7)/9))[-1]
			# Убираем возможные ведущие нули
			number = str(int(number))
			# Небольшая задержка для изменения времени
			sleep(0.0001)
		return int(number)

	@staticmethod
	def random() -> float:
		""" Возвращает случайное число с плавающей точкой в диапазоне [0.0, 1.0) """
		return float("0."+str(PseudoRandom.get_random_number(16)))
	
	@staticmethod
	def random_from_range(start: int, end: int) -> int:
		""" Возвращает случайно выбранный элемент из диапазона [start, end) """ 
		return int(true_round((end-start)*(PseudoRandom.random())+start))
	
	@staticmethod
	def random_from_float_range(start, end) -> float:
		"""
  		Возвращает случайно выбранное число с плавающей точкой из диапазона [start, end)
  		
		start, end - могут быть как целыми числами, так и числами с плавающей точкой
    	"""
		return ((end-start)*(PseudoRandom.random())+start)
	
	@staticmethod
	def choice(array):
		""" Возвращает случайно выбранный элемент из непустого массива """
		return array[int(PseudoRandom.random_from_range(0, len(array)))]
	
	@staticmethod
	def shuffle(array):
		""" Перемешивает массив на месте """
		for _ in range(len(array)*2):
			x1, x2 = int(PseudoRandom.random_from_range(0, len(array)-1)), int(PseudoRandom.random_from_range(0, len(array)-1))
			array[x1], array[x2] = array[x2], array[x1]
