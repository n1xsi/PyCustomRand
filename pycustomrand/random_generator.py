from .custom_round import true_round
from time import sleep, time_ns


class PseudoRandom:
    # Переменная класса для хранения seed генератора псевдослучайных чисел
    _seed = None

    @classmethod
    def set_seed(cls, seed=None) -> None:
        """
        Установка нового значения seed для генератора псевдослучайных чисел.

        seed - любой объект, который можно преобразовать в строку.
        """
        if seed is not None:
            cls._seed = sum(map(ord, str(seed)))

    @staticmethod
    def _get_next_seed_state(current_seed: int) -> int:
        """ 
        Вспомогательная функция - меняет состояние зерна.
        Используется линейный конгруэнтный метод для сильного изменения зерна на каждом шаге.
        (Константы взяты из Borland C/C++ runtime library)
        """
        return (current_seed * 22695477 + 1) & 0xFFFFFFFF

    @classmethod
    def get_random_number(cls, length: int = 1) -> int:
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
        raw_int = PseudoRandom.get_random_number(16)
        raw_str = str(raw_int).zfill(16)
        return float("0." + raw_str)

    @staticmethod
    def random_from_range(start: int, end: int) -> int:
        """Возвращает случайно выбранный элемент из диапазона [start, end)."""
        return int(true_round((end - start) * (PseudoRandom.random()) + start))

    @staticmethod
    def random_from_float_range(start, end) -> float:
        """
        Возвращает случайно выбранное число с плавающей точкой из диапазона [start, end)

        start, end - могут быть как целыми числами, так и числами с плавающей точкой
        """
        return ((end-start) * (PseudoRandom.random()) + start)

    @staticmethod
    def choice(array) -> None:
        """Возвращает случайно выбранный элемент из непустого массива."""
        return array[int(PseudoRandom.random_from_range(0, len(array)))]

    @staticmethod
    def shuffle(array) -> None:
        """Перемешивает массив на месте."""
        limit = len(array)-1
        for _ in range(len(array)*2):
            x1, x2 = int(PseudoRandom.random_from_range(0, limit)), int(PseudoRandom.random_from_range(0, limit))
            array[x1], array[x2] = array[x2], array[x1]
