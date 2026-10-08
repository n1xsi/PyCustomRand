# Делает класс PseudoRandom доступным при импорте пакета
from .random_generator import PseudoRandom
from .custom_round import true_round

# Версия пакета
__version__ = "0.0.4"

# Алиасы для основных функций
set_seed = PseudoRandom.set_seed
gen_random_number = PseudoRandom.gen_random_number
random = PseudoRandom.random

# Алиасы для целых чисел
randrange = PseudoRandom.randrange
random_integer = PseudoRandom.random_integer
randint = PseudoRandom.random_integer

# Алиасы для чисел с плавающей точкой
random_float = PseudoRandom.random_float

# Алиасы для байтовых функций
random_bytes = PseudoRandom.random_bytes

# Алиасы для последовательностей
choice = PseudoRandom.choice
choices = PseudoRandom.choices
shuffle = PseudoRandom.shuffle
sample = PseudoRandom.sample

# Алиасы для распределений
triangular = PseudoRandom.triangular
gauss = PseudoRandom.gauss
expovariate = PseudoRandom.expovariate
binomialvariate = PseudoRandom.binomialvariate
binomial = PseudoRandom.binomialvariate

# Алиасы для утилит
random_bool = PseudoRandom.random_bool
random_uuid4 = PseudoRandom.random_uuid4
random_color_hex = PseudoRandom.random_color_hex

# Для "from pycustomrand import *"
__all__ = [
    "PseudoRandom",
    "true_round",
    "random",
    "set_seed",
    "gen_random_number",
    "randrange",
    "random_integer",
    "randint",
    "random_float",
    "random_bytes",
    "choice",
    "choices",
    "shuffle",
    "sample",
    "triangular",
    "gauss",
    "expovariate",
    "binomial",
    "binomialvariate",
    "random_bool",
    "random_uuid4",
    "random_color_hex"
]
