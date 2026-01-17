from .custom_round import true_round
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
    def random_from_range(start: int, end: int) -> int:
        """Возвращает случайно выбранный элемент из диапазона [start, end]."""
        return true_round((end - start) * (PseudoRandom.random()) + start)


    # -------------------- Функции для чисел с плавающей точкой --------------------

    @staticmethod
    def random_float(start: int | float, end: int | float, digits: int = None) -> float:
        """
        Возвращает случайно выбранное число с плавающей точкой из диапазона [start, end).

        start, end - могут быть как целыми числами, так и числами с плавающей точкой.
        digits - количество знаков после запятой в возвращаемом числе. Если None - без округления.
        """
        result = (end-start) * (PseudoRandom.random()) + start
        if digits is not None:
            return true_round(result, digits)
        return result


    # -------------------- Байтовые функции --------------------

    @staticmethod
    def random_bytes(count: int) -> bytes:
        """Возвращает случайные байты в количестве count."""
        return bytes([PseudoRandom.random_from_range(0, 255) for _ in range(count)])


    # -------------------- Функции для последовательностей --------------------

    @staticmethod
    def choice(array: list[Any]) -> Any:
        """Возвращает случайно выбранный элемент из массива."""
        if not array:
            return None
        index = int(PseudoRandom.random() * len(array))
        return array[index]

    @staticmethod
    def shuffle(array: list[Any]) -> None:
        """Перемешивает массив на месте."""
        limit = len(array)-1
        for _ in range(len(array)*2):
            x1, x2 = PseudoRandom.random_from_range(0, limit), PseudoRandom.random_from_range(0, limit)
            array[x1], array[x2] = array[x2], array[x1]
