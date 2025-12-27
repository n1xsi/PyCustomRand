def true_round(number: float | int, length: int = 0) -> float | int:
    # Если пришёл int - сразу возвращаем int
    if isinstance(number, int):
        return number

    # Получение цифр после запятой заданного числа
    number_parts = str(number).split('.')
    # Определение знака числа
    sign = -1 if number_parts[0][0] == '-' else 1
    # Создаём список цифр из числа (digits[0] - целая часть со знаком, digits[1] - дробная)
    digits = [abs(int(number_parts[0]))] + list(map(int, number_parts[1]))

    # Проход по цифрам в обратном порядке, начиная с той, что после нужного знака округления
    ## "-1", т.к. первое значение в digits - это целая часть числа
    ## (1 if length == 0 else 0) - корректная обработка округления до целого числа - проходимся по всем цифрам
    # до первой цифры после запятой включительно
    for i in range(len(digits)-1-(1 if length == 0 else 0), length-1-(1 if length == 0 else -1), -1):
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
        # используем split('.')[0], чтобы сохранить знак перед числом (+/-)
        return (float(digits[0]) + (1 if digits[1] >= 5 else 0))*sign
    else:
        # Иначе формируем и возвращаем число с заданным кол-вом знаков после запятой
        return float(f"{digits[0]}.{''.join(map(str, digits[1:length+1]))}")*sign
