# Модуль для фильтрации логов
# Здесь мы фильтруем логи по разным критериям

import config  # импортируем настройки

def filter_by_keyword(logs, keyword):
    """
    Фильтрует логи по ключевому слову
    """
    filtered_logs = []  # создаем пустой список для отфильтрованных логов
    
    # Проходим по всем логам
    for log in logs:
        # Проверяем, содержится ли ключевое слово в сырой строке
        if 'raw' in log and keyword.lower() in log['raw'].lower():
            filtered_logs.append(log)  # добавляем лог в список
    
    return filtered_logs  # возвращаем отфильтрованные логи

def filter_by_level(logs, level):
    """
    Фильтрует логи по уровню важности
    """
    filtered_logs = []  # создаем пустой список
    
    # Проходим по всем логам
    for log in logs:
        raw_text = log.get('raw', '').lower()  # получаем текст лога в нижнем регистре
        
        # Проверяем уровень
        if level == 'ERROR':
            # Для ошибок проверяем наличие ключевых слов ошибок
            for keyword in config.ERROR_KEYWORDS:
                if keyword.lower() in raw_text:
                    filtered_logs.append(log)  # добавляем лог
                    break  # выходим из цикла проверки ключевых слов
        
        elif level == 'WARNING':
            # Для предупреждений проверяем наличие ключевых слов предупреждений
            for keyword in config.WARNING_KEYWORDS:
                if keyword.lower() in raw_text:
                    filtered_logs.append(log)  # добавляем лог
                    break  # выходим из цикла
        
        elif level == 'INFO':
            # Для информационных сообщений
            # Если нет ключевых слов ошибок и предупреждений
            is_error = any(keyword.lower() in raw_text for keyword in config.ERROR_KEYWORDS)
            is_warning = any(keyword.lower() in raw_text for keyword in config.WARNING_KEYWORDS)
            
            if not is_error and not is_warning:
                filtered_logs.append(log)  # добавляем лог
    
    return filtered_logs  # возвращаем отфильтрованные логи

def filter_by_type(logs, log_type):
    """
    Фильтрует логи по типу
    """
    filtered_logs = []  # создаем пустой список
    
    # Проходим по всем логам
    for log in logs:
        # Проверяем тип лога
        if log.get('type') == log_type:
            filtered_logs.append(log)  # добавляем лог
    
    return filtered_logs  # возвращаем отфильтрованные логи

def advanced_filter(logs, keywords=None, level=None, log_type=None):
    """
    Продвинутая фильтрация по нескольким критериям
    """
    filtered_logs = logs  # начинаем со всех логов
    
    # Применяем фильтр по ключевым словам
    if keywords:
        temp_logs = []  # временный список
        for log in filtered_logs:
            # Проверяем каждое ключевое слово
            for keyword in keywords:
                if keyword.lower() in log.get('raw', '').lower():
                    temp_logs.append(log)  # добавляем лог
                    break  # выходим из цикла проверки
        filtered_logs = temp_logs  # обновляем список
    
    # Применяем фильтр по уровню
    if level:
        filtered_logs = filter_by_level(filtered_logs, level)
    
    # Применяем фильтр по типу
    if log_type:
        filtered_logs = filter_by_type(filtered_logs, log_type)
    
    return filtered_logs  # возвращаем окончательный список