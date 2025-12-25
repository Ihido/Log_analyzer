# Модуль для статистики логов
# Здесь мы считаем статистику и генерируем отчеты

import config  # импортируем настройки
from collections import Counter  # импортируем Counter для подсчета

def count_errors(logs):
    """
    Считает количество ошибок
    """
    error_count = 0  # счетчик ошибок
    
    # Проходим по всем логам
    for log in logs:
        raw_text = log.get('raw', '').lower()  # текст лога в нижнем регистре
        
        # Проверяем наличие ключевых слов ошибок
        for keyword in config.ERROR_KEYWORDS:
            if keyword.lower() in raw_text:
                error_count += 1  # увеличиваем счетчик
                break  # выходим из цикла проверки
    
    return error_count  # возвращаем количество ошибок

def count_warnings(logs):
    """
    Считает количество предупреждений
    """
    warning_count = 0  # счетчик предупреждений
    
    # Проходим по всем логам
    for log in logs:
        raw_text = log.get('raw', '').lower()  # текст лога в нижнем регистре
        
        # Проверяем наличие ключевых слов предупреждений
        for keyword in config.WARNING_KEYWORDS:
            if keyword.lower() in raw_text:
                warning_count += 1  # увеличиваем счетчик
                break  # выходим из цикла проверки
    
    return warning_count  # возвращаем количество предупреждений

def get_level_distribution(logs):
    """
    Распределение логов по уровням важности
    """
    levels = {'ERROR': 0, 'WARNING': 0, 'INFO': 0}  # словарь для подсчета
    
    # Проходим по всем логам
    for log in logs:
        raw_text = log.get('raw', '').lower()  # текст лога в нижнем регистре
        
        # Проверяем на ошибки
        is_error = False
        for keyword in config.ERROR_KEYWORDS:
            if keyword.lower() in raw_text:
                levels['ERROR'] += 1  # увеличиваем счетчик ошибок
                is_error = True
                break
        
        # Если не ошибка, проверяем на предупреждения
        if not is_error:
            is_warning = False
            for keyword in config.WARNING_KEYWORDS:
                if keyword.lower() in raw_text:
                    levels['WARNING'] += 1  # увеличиваем счетчик предупреждений
                    is_warning = True
                    break
            
            # Если не ошибка и не предупреждение
            if not is_warning:
                levels['INFO'] += 1  # увеличиваем счетчик информационных сообщений
    
    return levels  # возвращаем распределение

def get_top_errors(logs, top_n=10):
    """
    Возвращает топ-N самых частых ошибок
    """
    error_messages = []  # список для сообщений об ошибках
    
    # Собираем сообщения об ошибках
    for log in logs:
        raw_text = log.get('raw', '')  # получаем текст лога
        
        # Проверяем, является ли лог ошибкой
        for keyword in config.ERROR_KEYWORDS:
            if keyword.lower() in raw_text.lower():
                error_messages.append(raw_text)  # добавляем сообщение
                break
    
    # Считаем частоту ошибок
    error_counter = Counter(error_messages)  # создаем счетчик
    
    # Получаем самые частые ошибки
    top_errors = error_counter.most_common(top_n)
    
    return top_errors  # возвращаем топ ошибок

def generate_report(logs):
    """
    Генерирует полный отчет по логам
    """
    # Считаем общую статистику
    total_logs = len(logs)  # общее количество логов
    errors = count_errors(logs)  # количество ошибок
    warnings = count_warnings(logs)  # количество предупреждений
    
    # Получаем распределение по уровням
    levels = get_level_distribution(logs)
    
    # Получаем топ ошибок
    top_errors = get_top_errors(logs, 5)
    
    # Создаем отчет
    report = {
        'total_logs': total_logs,  # общее количество
        'errors': errors,          # количество ошибок
        'warnings': warnings,      # количество предупреждений
        'levels': levels,          # распределение по уровням
        'top_errors': top_errors   # топ ошибок
    }
    
    return report  # возвращаем отчет

def print_report(report):
    """
    Красиво выводит отчет на экран
    """
    print("=" * 50)  # разделительная линия
    print("ОТЧЕТ АНАЛИЗАТОРА ЛОГОВ")  # заголовок
    print("=" * 50)  # разделительная линия
    
    # Выводим основную статистику
    print(f"\nОБЩАЯ СТАТИСТИКА:")
    print(f"  Всего записей: {report['total_logs']}")  # общее количество
    print(f"  Ошибок: {report['errors']}")  # ошибки
    print(f"  Предупреждений: {report['warnings']}")  # предупреждения
    
    # Выводим распределение по уровням
    print(f"\nРАСПРЕДЕЛЕНИЕ ПО УРОВНЯМ:")
    for level, count in report['levels'].items():
        percentage = (count / report['total_logs'] * 100) if report['total_logs'] > 0 else 0
        print(f"  {level}: {count} ({percentage:.1f}%)")  # уровень и процент
    
    # Выводим топ ошибок
    if report['top_errors']:
        print(f"\nТОП-5 САМЫХ ЧАСТЫХ ОШИБОК:")
        for i, (error, count) in enumerate(report['top_errors'], 1):
            print(f"  {i}. [{count} раз] {error[:100]}...")  # выводим первые 100 символов
    
    print("\n" + "=" * 50)  # разделительная линия