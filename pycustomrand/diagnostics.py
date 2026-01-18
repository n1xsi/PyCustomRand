from collections import defaultdict
from functools import wraps
from time import time


def check_distribution(count: int = 1000, buckets: int = 10):
    """
    Декоратор для проверки равномерности распределения генератора.

    count - сколько раз запустить генератор.
    buckets - на сколько частей разбить диапазон [0, 1).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"===== Запуск анализа распределения ({count} итераций) =====")
            start_time = time()
            previous_time = start_time

            # Словарь для подсчета попаданий
            stats = defaultdict(int)

            for i in range(count):
                # Каждые 5 секунд вывод текущей итерации
                current_time = time()
                if current_time - previous_time > 5:
                    print(f"Нынешняя итерация: {i}")
                    previous_time = current_time

                val = func(*args, **kwargs)
                # Превращение числа 0.0-1.0 в номер корзины (0, 1, ..., buckets-1)
                # int() для корзин равного размера
                bucket_index = int(val * buckets)

                # Защита от граничного случая, если выпадет ровно 1.0
                if bucket_index == buckets:
                    bucket_index -= 1

                stats[bucket_index] += 1

            elapsed = time() - start_time
            print(f"Генерация завершена за {elapsed:.4f} сек.\n")

            # Анализ результатов
            expected_percent = 100 / buckets
            print(f"{'Корзина':<10} | {'Кол-во':<10} | {'%':<10} | {'Отклонение':<10}")
            print("=" * 50)

            max_diff = 0

            for k in sorted(stats.keys()):
                v = stats[k]
                percent = (v / count) * 100
                diff = abs(percent - expected_percent)
                if diff > max_diff:
                    max_diff = diff

                print(f"{k:<10} | {v:<10} | {percent:<10.2f}% | {diff:<10.2f}%")

            print("=" * 50)
            print(f"Максимальное отклонение: {max_diff:.4f}%")
            if max_diff < 1.0:
                print(">> РЕЗУЛЬТАТ: Отличное равномерное распределение!")
            else:
                print(">> РЕЗУЛЬТАТ: Есть перекосы (вероятно, мала выборка или проблема в алгоритме).")

            # Возврат последнего сгенерированного числа, чтобы не ломать логику программы
            return val

        return wrapper
    return decorator
