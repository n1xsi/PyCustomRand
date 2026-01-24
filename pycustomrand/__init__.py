# Делает класс PseudoRandom доступным при импорте пакета
from .random_generator import PseudoRandom
from .custom_round import true_round

# Версия пакета
__version__ = "0.0.1"


# -------------------- Алиасы --------------------

# Основные функции
set_seed = PseudoRandom.set_seed
gen_random_number = PseudoRandom.gen_random_number
random = PseudoRandom.random

# Целые числа
randrange = PseudoRandom.randrange
random_integer = PseudoRandom.random_integer
randint = PseudoRandom.random_integer

# Числа с плавающей точкой
random_float = PseudoRandom.random_float

# Байтовые функции
random_bytes = PseudoRandom.random_bytes

# Последовательности
choice = PseudoRandom.choice
choices = PseudoRandom.choices
shuffle = PseudoRandom.shuffle
sample = PseudoRandom.sample

# Распределения
triangular = PseudoRandom.triangular
gauss = PseudoRandom.gauss
expovariate = PseudoRandom.expovariate
binomialvariate = PseudoRandom.binomialvariate
binomial = PseudoRandom.binomialvariate

# Утилиты
random_bool = PseudoRandom.random_bool
random_uuid4 = PseudoRandom.random_uuid4
random_color_hex = PseudoRandom.random_color_hex

# ------------------------------------------------

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
