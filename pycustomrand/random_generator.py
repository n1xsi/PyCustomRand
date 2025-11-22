from .custom_round import true_round
import time


class PseudoRandom:
	@staticmethod
	def get_random_number(length=1):
		number = ''
		while len(number) != length:
            # magic starts here
			number += (str(int(((int(str(int((time.time_ns()*1.71)/0.8))[::-1])**0.5)*7)/9))[-1])
			number = str(int(number))
			time.sleep(0.001)
		return int(number)

	@staticmethod
	def random():
		return float("0."+str(PseudoRandom.get_random_number(16)))
	
	@staticmethod
	def random_from_range(start, end):
		return true_round((end-start)*(PseudoRandom.random())+start)
	
	@staticmethod
	def random_from_float_range(start, end):
		return ((end-start)*(PseudoRandom.random())+start)
	
	@staticmethod
	def choice(array):
		return array[int(PseudoRandom.random_from_range(0, len(array)))]
	
	@staticmethod
	def shuffle(array):
		for _ in range(len(array)*2):
			x1, x2 = int(PseudoRandom.random_from_range(0, len(array)-1)), int(PseudoRandom.random_from_range(0, len(array)-1))
			array[x1], array[x2] = array[x2], array[x1]
