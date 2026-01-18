from .custom_round import true_round
from math import sqrt, log, cos, pi
from time import sleep, time_ns
from typing import Any


class PseudoRandom:
    # Переменная класса для хранения seed генератора псевдослучайных чисел
    _seed = None

    # -------------------- Основные функции генерации случайных чисел --------------------

    @classmethod
    def set_seed(cls, seed: Any = None) -> None:
        """
        Установка нового значения seed.

        seed - любой объект, который преобразуется в строку. Если None - сброс на время (time_ns()).
        """
        if seed is not None:
            cls._seed = sum(map(ord, str(seed)))
        else:
            cls._seed = None

    @staticmethod
    def _get_next_seed_state(current_seed: int) -> int:
        """
        Вспомогательная функция - меняет состояние зерна с помощью линейного конгруэнтного метода.
        (Константы взяты из Borland C/C++ runtime library.)
        """
        return (current_seed * 22695477 + 1) & 0xFFFFFFFF

    @classmethod
    def gen_random_number(cls, length: int = 1) -> int:
        """Генерация псевдослучайного числа заданной длины."""
        number = ''
        while len(number) != length:
            # Определение источника энтропии (время или seed)
            if cls._seed is not None:
                is_seeded = True
                current_entropy = cls._seed
                # Обновление seed для следующей итерации (цифры), иначе результат будет одинаковым
                cls._seed = cls._get_next_seed_state(cls._seed)
            else:
                is_seeded = False
                current_entropy = time_ns()

            # Генерация псевдослучайного числа на основе текущей энтропии и "волшебных" математических операций
            calc_base = int((current_entropy * 1.71) / 0.8)
            reversed_base = int(str(calc_base)[::-1])
            magic_result = ((reversed_base ** 0.5) * 7) / 9

            # Добавление последней цифры результата
            number += str(int(magic_result))[-1]

            # Если нет seed, нужна задержка, чтобы время изменилось (т.к. entropy - время)
            if not is_seeded:
                sleep(0.0001)

        return int(number)

    @staticmethod
    def random() -> float:
        """Возвращает случайное число с плавающей точкой в диапазоне [0.0, 1.0)."""
        raw_int = PseudoRandom.gen_random_number(16)
        raw_str = str(raw_int).zfill(16)
        return float("0." + raw_str)

    # -------------------- Числовые функции --------------------

    @staticmethod
    def randrange(start: int, stop: int = None, step: int = 1) -> int:
        """
        Возвращает случайное число из диапазона [start, stop).
        Верхняя граница НЕ включается. Можно указывать один аргумент.

        Примеры:
        randrange(10) -> от 0 до 9
        randrange(1, 10) -> от 1 до 9
        randrange(0, 10, 2) -> чётное число от 0 до 8
        """
        if stop is None:
            # Если передан один аргумент, например randrange(10), то считаем его за stop, а start за 0
            stop = start
            start = 0

        range_object = range(start, stop, step)

        if not range_object:
            raise ValueError("Пустой диапазон для генерации")

        return range_object[int(PseudoRandom.random() * len(range_object))]

    @staticmethod
    def random_integer(start: int, end: int = None, step: int = 1) -> int:
        """
        Возвращает случайное число из диапазона [start, end].
        Включительны и обязательны обе границы.

        step (опциональный аргумент) - число должно делиться на step (относительно start)
        """
        if step == 0:
            raise ValueError("Step (шаг) не может быть равен 0")

        # Длина диапазона
        width = end - start

        # Количество шагов = (разница / шаг) + 1
        n_steps = int(width / step) + 1

        if n_steps <= 0:
            raise ValueError("Неверные границы диапазона для заданного шага")

        # Выбор случайного индекса шага
        random_step_index = int(PseudoRandom.random() * n_steps)

        return start + (random_step_index * step)

    # -------------------- Функции для чисел с плавающей точкой --------------------

    @staticmethod
    def random_float(start: int | float, end: int | float, digits: int = None) -> float:
        """
        Возвращает случайноe число с плавающей точкой из диапазона [start, end)
        или [start, end] в зависимости от округления (при наличии digits).

        start, end - могут быть как целыми числами, так и числами с плавающей точкой.
        digits - количество знаков после запятой в возвращаемом числе. Если None - без округления.
        """
        result = (end-start) * (PseudoRandom.random()) + start
        if digits is not None:
            return true_round(result, digits)
        return result

    @staticmethod
    def triangular(low: float = 0.0, high: float = 1.0, mode: float = None) -> float:
        """
        Возвращает случайное число с треугольным распределением в диапазоне [low, high].
        Чаще всего выпадает значение около mode (вершина треугольника).
        """
        uniform = PseudoRandom.random()
        cutoff = 0.5 if mode is None else (mode - low) / (high - low)
        if uniform > cutoff:
            uniform = 1.0 - uniform
            cutoff = 1.0 - cutoff
            low, high = high, low
        return low + (high - low) * (uniform * cutoff) ** 0.5

    @staticmethod
    def gauss(mu: float = 0.0, sigma: float = 1.0) -> float:
        """
        Возвращает случайное число с нормальным (гауссовым) распределением.
        Алгоритм Бокса-Мюллера.

        mu - среднее значение, центр колокола (математическое ожидание).
        sigma - стандартное отклонение, ширина колокола.
        """
        u1 = PseudoRandom.random()
        u2 = PseudoRandom.random()
        z0 = sqrt(-2.0 * log(u1)) * cos(2.0 * pi * u2)
        return z0 * sigma + mu

    @staticmethod
    def expovariate(lambd: float = 1.0) -> float:
        """
        Возвращает случайное число с экспоненциальным распределением.

        lambd - параметр интенсивности (должен быть не 0).
        """
        return -log(1 - PseudoRandom.random()) / lambd

    # -------------------- Байтовые функции --------------------

    @staticmethod
    def random_bytes(count: int) -> bytes:
        """Возвращает случайные байты в количестве count."""
        return bytes([PseudoRandom.random_integer(0, 255) for _ in range(count)])

    # -------------------- Функции для последовательностей --------------------

    @staticmethod
    def choice(array: list[Any]) -> Any:
        """Возвращает случайно выбранный элемент из массива."""
        if not array:
            return None
        index = PseudoRandom.randrange(len(array))
        return array[index]

    @staticmethod
    def choices(array: list[Any], k: int, weights: list[int] = None) -> list[Any]:
        """
        Возвращает список из k случайных элементов из массива (с повторениями).

        weights - список с весами для каждого элемента массива (соответствует по индексу).
        Если None - все элементы считаются равными (по 1 весу).
        """
        if weights is None:
            weights = [1] * len(array)

        if len(array) != len(weights):
            raise ValueError("Длина массива и длина weights должны быть равны")

        weighted_array = []
        for item, weight in zip(array, weights):
            weighted_array.extend([item] * weight)

        return [PseudoRandom.choice(weighted_array) for _ in range(k)]

    @staticmethod
    def shuffle(array: list[Any]) -> None:
        """Перемешивает массив на месте."""
        for i in range(len(array) - 1, 0, -1):
            j = PseudoRandom.randrange(i + 1)
            array[i], array[j] = array[j], array[i]

    @staticmethod
    def sample(array: list[Any], k: int, counts: list[int] = None) -> list[Any]:
        """
        Возвращает список из k уникальных случайных элементов из массива.

        counts - список с количеством повторений для каждого элемента массива (соответствует по индексу).
        Если None - все элементы считаются равными (по 1 повторению).
        """
        if counts is None:
            counts = [1] * len(array)

        if len(array) != len(counts):
            raise ValueError("Длина массива и длина counts должны быть равны")

        weighted_array = []
        for item, count in zip(array, counts):
            weighted_array.extend([item] * count)

        if k > len(set(weighted_array)):
            raise ValueError("k не может быть больше количества уникальных элементов в массиве с учётом counts")

        result = []
        while len(result) < k:
            choice = PseudoRandom.choice(weighted_array)
            if choice not in result:
                result.append(choice)

        return result

    # -------------------- Дискретные функции --------------------

    @staticmethod
    def binomialvariate(n: int = 1, p: float = 0.5) -> int:
        """
        Возвращает случайное число, распределённое по биномиальному закону.
        Простейшая реализация, неоптимизированная.

        n - количество испытаний (целое число >= 0).
        p - вероятность успеха в каждом испытании (0.0 <= p <= 1.0).
        """
        if n < 0:
            raise ValueError("Количество испытаний n не может быть отрицательным")
        if not (0.0 <= p <= 1.0):
            raise ValueError("Вероятность p должна быть в диапазоне [0, 1]")

        return sum([PseudoRandom.random() < p for _ in range(n)])
