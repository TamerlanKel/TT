def appearance(intervals: dict[str, list[int]]) -> int:
    # Извлекаем интервалы из словаря
    lesson_start, lesson_end = intervals['lesson']
    pupil_intervals = intervals['pupil']
    tutor_intervals = intervals['tutor']

    # Функция для обработки и нормализации интервалов
    def process_intervals(times, start_limit, end_limit):
        # Разбиваем список на пары (вход, выход)
        pairs = [(times[i], times[i + 1]) for i in range(0, len(times), 2)]
        # Обрезаем интервалы по границам урока
        processed = []
        for enter, exit in pairs:
            # Интервал должен быть валидным (enter < exit) и пересекаться с уроком
            if enter < exit and exit > start_limit and enter < end_limit:
                # Обрезаем по границам урока
                clipped_enter = max(enter, start_limit)
                clipped_exit = min(exit, end_limit)
                processed.append((clipped_enter, clipped_exit))
        # Сортируем интервалы по времени входа
        processed.sort()
        return processed

    # Обрабатываем интервалы ученика и учителя
    pupil = process_intervals(pupil_intervals, lesson_start, lesson_end)
    tutor = process_intervals(tutor_intervals, lesson_start, lesson_end)

    # Ищем пересечения интервалов ученика и учителя
    total = 0
    i = j = 0

    while i < len(pupil) and j < len(tutor):
        # Текущие интервалы
        p_start, p_end = pupil[i]
        t_start, t_end = tutor[j]

        # Находим пересечение
        intersect_start = max(p_start, t_start)
        intersect_end = min(p_end, t_end)

        # Если есть пересечение - добавляем его длительность
        if intersect_start < intersect_end:
            total += intersect_end - intersect_start

        # Переходим к следующему интервалу того, кто раньше закончился
        if p_end < t_end:
            i += 1
        else:
            j += 1

    return total