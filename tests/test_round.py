from pycustomrand.custom_round import true_round
import unittest


class TestTrueRound(unittest.TestCase):

    # -------------------- Базовые тесты --------------------

    def test_integers(self):
        """Проверка: целые числа не должны меняться."""
        self.assertEqual(true_round(5), 5)
        self.assertEqual(true_round(0), 0)
        self.assertEqual(true_round(100), 100)

    def test_basic_rounding_down(self):
        """Проверка: округление вниз."""
        self.assertEqual(true_round(1.1), 1)
        self.assertEqual(true_round(1.4), 1)
        self.assertEqual(true_round(1.4999), 2)

    def test_basic_rounding_up(self):
        """Проверка: округление вверх (числа > 0.5)."""
        self.assertEqual(true_round(1.6), 2)
        self.assertEqual(true_round(1.9), 2)
        self.assertEqual(true_round(0.99), 1)

    def test_rounding_half_up(self):
        """
        ГЛАВНАЯ ПРОВЕРКА: Округление 0.5
        В стандартном Python round(2.5) == 2 (банковское округление).
        Функция true_round должна давать 3 (математическое округление).
        """
        self.assertEqual(true_round(0.5), 1)
        self.assertEqual(true_round(1.5), 2)
        self.assertEqual(true_round(2.5), 3)
        self.assertEqual(true_round(3.5), 4)

    def test_precision_1_digit(self):
        """Проверка: округление до 1 знака"""
        self.assertEqual(true_round(0.14, 1), 0.1)
        self.assertEqual(true_round(0.15, 1), 0.2)
        self.assertEqual(true_round(0.16, 1), 0.2)

    def test_precision_cascade(self):
        """
        Проверка каскадного округления.
        Пример: 1.99 при округлении до 1 знака должно стать 2.0
        """
        self.assertEqual(true_round(1.99, 1), 2.0)
        self.assertEqual(true_round(9.99, 1), 10.0)

        # Проверка сложного случая: 0.445 -> 0.45 -> 0.5 (при округлении до 1 знака)
        self.assertEqual(true_round(0.445, 1), 0.5)

    # -------------------- Продвинутые тесты --------------------

    def test_float_representation_fix(self):
        """
        Тест на 'проблему 2.675'.
        Стандартный round(2.675, 2) дает 2.67.
        Математическое округление должно давать 2.68.
        """
        self.assertEqual(true_round(2.675, 2), 2.68)
        self.assertEqual(true_round(1.005, 2), 1.01)

    def test_heavy_cascade(self):
        """
        Тест 'Эффект Домино'.
        9.999 при округлении до 2 знаков должно стать 10.0
        """
        # 9.999 -> 9.9(9+1) -> 9.(9+1)0 -> (9+1).00 -> 10.0
        self.assertEqual(true_round(9.999, 2), 10.0)

        # 89.999 -> 90.0
        self.assertEqual(true_round(89.999, 2), 90.0)

    def test_small_numbers(self):
        """Работа с очень маленькими числами."""
        # 0.0005 -> округляем до 3 знаков -> 0.001
        self.assertEqual(true_round(0.0005, 3), 0.001)

        # 0.0004 -> округляем до 3 знаков -> 0.0
        self.assertEqual(true_round(0.0004, 3), 0.0)

    def test_rounding_to_zero_length(self):
        """
        Явное указание length=0.
        Должно работать так же, как без указания length.
        """
        self.assertEqual(true_round(5.6, 0), 6)
        self.assertIsInstance(true_round(5.6, 0), int)

    def test_negative_numbers(self):
        """
        Отрицательные числа.
        Математически: -1.5 округляется до -2 (по модулю).
        """
        self.assertEqual(true_round(-1.5), -2)
        self.assertEqual(true_round(-1.1), -1)


if __name__ == '__main__':
    unittest.main()
