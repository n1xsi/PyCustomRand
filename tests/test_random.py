from pycustomrand.random_generator import PseudoRandom
import unittest


class TestPseudoRandom(unittest.TestCase):

    def setUp(self):
        """Выполняется перед каждым тестом"""
        # Сброс сида перед каждым тестом (для чистоты)
        PseudoRandom.set_seed(None)

    def test_reproducibility_with_seed(self):
        """Главный тест: проверка работы Seed"""
        seed_value = "TestSeed123"

        # Запуск 1
        PseudoRandom.set_seed(seed_value)
        val1 = PseudoRandom.random()
        val2 = PseudoRandom.random_integer(0, 100)

        # Запуск 2 (с тем же сидом)
        PseudoRandom.set_seed(seed_value)
        val1_again = PseudoRandom.random()
        val2_again = PseudoRandom.random_integer(0, 100)

        self.assertEqual(val1, val1_again, "Seed не работает: float значения разные")
        self.assertEqual(val2, val2_again, "Seed не работает: integer значения разные")

    def test_randrange_bounds(self):
        """Проверка границ randrange"""
        for _ in range(100):
            val = PseudoRandom.randrange(0, 5)
            self.assertGreaterEqual(val, 0)
            self.assertLess(val, 5)  # Строго меньше 5

    def test_random_integer_bounds(self):
        """Проверка границ random_integer (включительно)"""
        found_max = False
        for _ in range(200):
            val = PseudoRandom.random_integer(1, 3)
            self.assertGreaterEqual(val, 1)
            self.assertLessEqual(val, 3)
            if val == 3:
                found_max = True
        # Надежда на то, что за 200 попыток хоть раз выпадет 3 (верхняя граница)
        self.assertTrue(found_max, "Верхняя граница random_integer не достигается")

    def test_choice_error(self):
        """Проверка, что пустой массив возвращает None"""
        self.assertIsNone(PseudoRandom.choice([]))

    def test_random_bytes_length(self):
        """Проверка длины байтов"""
        b = PseudoRandom.random_bytes(10)
        self.assertEqual(len(b), 10)
        self.assertIsInstance(b, bytes)

    def test_uuid4_format(self):
        """Проверка формата UUID (если ты добавил эту функцию)"""
        if hasattr(PseudoRandom, 'uuid4'):
            uuid = PseudoRandom.uuid4()
            self.assertEqual(len(uuid), 36)
            self.assertEqual(uuid[14], '4')  # Версия UUID всегда 4
            self.assertIn(uuid[19], ['8', '9', 'a', 'b'])  # Вариант UUID


if __name__ == '__main__':
    unittest.main()
