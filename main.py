# Главный файл анализатора логов
# Отсюда запускается вся программа

import os  # импортируем модуль для работы с операционной системой
import sys  # импортируем системный модуль

# Импортируем функции из наших модулей
from log_parser import parse_log_file  # импортируем функцию парсинга
from log_filter import advanced_filter  # импортируем функцию фильтрации
from log_stats import generate_report, print_report  # импортируем функции статистики
import config  # импортируем настройки

def main():
    """
    Основная функция программы
    """
    print("Добро пожаловать в Анализатор логов!")  # приветствие
    print("=" * 50)  # разделительная линия
    
    # Запрашиваем путь к файлу логов
    log_path = input(f"Введите путь к файлу логов (по умолчанию: {config.DEFAULT_LOG_PATH}): ")
    
    # Если пользователь не ввел путь, используем путь по умолчанию
    if not log_path:
        log_path = config.DEFAULT_LOG_PATH
    
    # Проверяем существование файла
    if not os.path.exists(log_path):
        print(f"Файл {log_path} не найден!")  # сообщение об ошибке
        print("Использую тестовые данные...")  # сообщение пользователю
        
        # Создаем тестовые логи
        test_logs = create_test_logs()
    else:
        # Парсим реальный файл логов
        print(f"Чтение файла: {log_path}")  # сообщение о чтении
        
        # Определяем тип лога
        log_type = input("Введите тип лога (apache, nginx, syslog, auto): ")
        if not log_type:
            log_type = 'auto'  # автоматическое определение
        
        # Парсим файл
        test_logs = parse_log_file(log_path, log_type)
        print(f"Прочитано {len(test_logs)} записей")  # выводим количество записей
    
    # Основной цикл программы
    while True:
        print("\n" + "=" * 50)  # разделительная линия
        print("МЕНЮ АНАЛИЗАТОРА ЛОГОВ:")  # заголовок меню
        print("1. Показать все логи")  # пункт меню
        print("2. Фильтровать логи")  # пункт меню
        print("3. Показать статистику")  # пункт меню
        print("4. Поиск по ключевому слову")  # пункт меню
        print("5. Выход")  # пункт меню
        print("=" * 50)  # разделительная линия
        
        # Запрашиваем выбор пользователя
        choice = input("Выберите действие (1-5): ")  # ввод выбора
        
        # Обрабатываем выбор
        if choice == '1':
            # Показываем все логи
            show_all_logs(test_logs)  # вызов функции
            
        elif choice == '2':
            # Фильтруем логи
            filter_logs(test_logs)  # вызов функции
            
        elif choice == '3':
            # Показываем статистику
            show_statistics(test_logs)  # вызов функции
            
        elif choice == '4':
            # Поиск по ключевому слову
            search_logs(test_logs)  # вызов функции
            
        elif choice == '5':
            # Выход из программы
            print("Выход из программы. До свидания!")  # прощание
            break  # выход из цикла
            
        else:
            # Неправильный выбор
            print("Неправильный выбор. Попробуйте снова.")  # сообщение об ошибке

def show_all_logs(logs):
    """
    Показывает все логи
    """
    print(f"\nВСЕ ЛОГИ ({len(logs)} записей):")  # заголовок
    
    # Проверяем, есть ли логи
    if not logs:
        print("Логи не найдены!")  # сообщение
        return
    
    # Показываем первые 20 логов
    for i, log in enumerate(logs[:20]):
        print(f"{i+1}. [{log.get('type', 'unknown')}] {log.get('raw', '')[:100]}...")  # краткая информация
    
    # Если логов больше 20
    if len(logs) > 20:
        print(f"... и еще {len(logs) - 20} записей")  # сообщение о количестве

def filter_logs(logs):
    """
    Фильтрует логи по критериям
    """
    print("\nФИЛЬТРАЦИЯ ЛОГОВ:")  # заголовок
    
    # Запрашиваем критерии фильтрации
    keyword_input = input("Введите ключевые слова (через запятую или оставьте пустым): ")  # ключевые слова
    level = input("Введите уровень (ERROR, WARNING, INFO или оставьте пустым): ")  # уровень
    log_type = input("Введите тип лога (apache, nginx, syslog или оставьте пустым): ")  # тип
    
    # Обрабатываем ключевые слова
    keywords = None
    if keyword_input:
        # Разделяем ключевые слова по запятой
        keywords = [k.strip() for k in keyword_input.split(',')]
    
    # Применяем фильтр
    filtered = advanced_filter(logs, keywords, level, log_type)  # фильтрация
    
    # Показываем результаты
    print(f"\nНайдено {len(filtered)} записей:")  # количество найденных
    
    # Показываем отфильтрованные логи
    for i, log in enumerate(filtered[:10]):
        print(f"{i+1}. {log.get('raw', '')[:100]}...")  # краткая информация
    
    # Если отфильтрованных логов больше 10
    if len(filtered) > 10:
        print(f"... и еще {len(filtered) - 10} записей")  # сообщение о количестве

def show_statistics(logs):
    """
    Показывает статистику логов
    """
    print("\nСТАТИСТИКА ЛОГОВ:")  # заголовок
    
    # Генерируем отчет
    report = generate_report(logs)  # генерация отчета
    
    # Выводим отчет
    print_report(report)  # вывод отчета

def search_logs(logs):
    """
    Ищет логи по ключевому слову
    """
    print("\nПОИСК ПО КЛЮЧЕВОМУ СЛОВУ:")  # заголовок
    
    # Запрашиваем ключевое слово
    keyword = input("Введите ключевое слово для поиска: ")  # ввод ключевого слова
    
    # Проверяем, ввели ли ключевое слово
    if not keyword:
        print("Ключевое слово не введено!")  # сообщение об ошибке
        return
    
    # Ищем логи
    found_logs = []  # список для найденных логов
    
    # Проходим по всем логам
    for log in logs:
        # Проверяем наличие ключевого слова
        if keyword.lower() in log.get('raw', '').lower():
            found_logs.append(log)  # добавляем лог
    
    # Показываем результаты
    print(f"\nНайдено {len(found_logs)} записей с '{keyword}':")  # количество найденных
    
    # Показываем найденные логи
    for i, log in enumerate(found_logs[:10]):
        print(f"{i+1}. {log.get('raw', '')[:150]}...")  # краткая информация
    
    # Если найденных логов больше 10
    if len(found_logs) > 10:
        print(f"... и еще {len(found_logs) - 10} записей")  # сообщение о количестве

def create_test_logs():
    """
    Создает тестовые логи для демонстрации
    """
    print("\nСоздание тестовых логов...")  # сообщение
    
    # Тестовые логи разных типов
    test_data = [
        # Apache логи
        '192.168.1.1 - - [10/Oct/2023:12:34:56 +0300] "GET /index.html HTTP/1.1" 200 1234',
        '192.168.1.2 - - [10/Oct/2023:12:35:01 +0300] "POST /login.php HTTP/1.1" 404 567',
        '192.168.1.3 - - [10/Oct/2023:12:36:10 +0300] "GET /admin.php HTTP/1.1" 500 789 ERROR: Database connection failed',
        
        # Nginx логи
        '192.168.1.100 - - [10/Oct/2023:12:40:00 +0300] "GET /style.css HTTP/1.1" 200 1234',
        '192.168.1.101 - - [10/Oct/2023:12:41:00 +0300] "GET /script.js HTTP/1.1" 304 0 WARNING: Deprecated API',
        
        # Системные логи
        'Oct 10 12:45:00 server01 kernel: ERROR: Out of memory',
        'Oct 10 12:46:00 server01 systemd: WARNING: Service restart failed',
        'Oct 10 12:47:00 server01 cron: INFO: Job completed successfully',
        'Oct 10 12:48:00 server01 sshd: ERROR: Failed password for user',
        'Oct 10 12:49:00 server01 apt: INFO: Package update available'
    ]
    
    # Парсим тестовые данные
    from log_parser import parse_apache_log, parse_nginx_log, parse_syslog
    
    logs = []  # список для логов
    
    # Проходим по тестовым данным
    for line in test_data:
        # Пробуем разные парсеры
        log = parse_apache_log(line)  # пробуем Apache парсер
        if not log:
            log = parse_nginx_log(line)  # пробуем Nginx парсер
        if not log:
            log = parse_syslog(line)  # пробуем системный парсер
        
        # Если не удалось разобрать
        if not log:
            log = {'type': 'test', 'raw': line, 'message': line}  # создаем тестовый лог
        
        logs.append(log)  # добавляем лог
    
    print(f"Создано {len(logs)} тестовых записей")  # сообщение о количестве
    return logs  # возвращаем логи

# Проверяем, запущен ли этот файл напрямую
if __name__ == "__main__":
    main()  # запускаем основную функцию