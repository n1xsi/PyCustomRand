def true_round(number: int | float, length: int = 0) -> int | float:
    # Если пришёл int - сразу возвращаем int
    if isinstance(number, int):
        return number

    # Получение цифр после запятой заданного числа
    number_parts = str(number).split('.')
    # Определение знака числа
    sign = -1 if number_parts[0][0] == '-' else 1
    # Создаём список цифр из числа (digits[0] - целая часть со знаком, digits[1] - дробная)
    digits = [abs(int(number_parts[0]))] + list(map(int, number_parts[1]))
    
    # Начало прохода: по цифрам в обратном порядке, начиная с той, что после нужного знака округления
    start = len(digits)-1-(1 if length == 0 else 0)
    # Конец прохода: до первой цифры после запятой включительно (или до конца числа, если length == 0)
    end = length-1-(-2 if length == 0 else -1)
    
    # Проход по цифрам в обратном порядке (логика округления)
    for i in range(start, end, -1):
        # Если цифра на текущей позиции >= 5, то +1 к предыдущей цифре (правило округления)
        if digits[i] >= 5:
            digits[i-1] += 1
            # Обработка каскадного округления
            if digits[i-1] == 10:
                digits[i-2] += 1
                digits[i-1] = 0
            digits[i] = 0

    # Если кол-во знаков после запятой (length) не было задано
    if length == 0:
        # Тогда округляем до целого числа (+1 к числу, если первая цифра после запятой >= 5)
        return (int(digits[0]) + (1 if digits[1] >= 5 else 0))*sign
    else:
        # Иначе формируем и возвращаем число с заданным кол-вом знаков после запятой
        return float(f"{digits[0]}.{''.join(map(str, digits[1:length+1]))}")*sign
