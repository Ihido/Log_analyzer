# Модуль для парсинга логов
# Здесь мы читаем и разбираем логи разных типов

import re  # импортируем модуль для работы с регулярными выражениями
from datetime import datetime  # импортируем модуль для работы с датой и временем

def parse_apache_log(log_line):
    """
    Парсит одну строку лога Apache
    """
    # Шаблон для разбора строки лога Apache
    pattern = r'(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+)'
    
    # Пытаемся найти совпадение с шаблоном
    match = re.match(pattern, log_line)
    
    # Проверяем, нашли ли мы совпадение
    if match:
        # Извлекаем данные из найденных групп
        ip_address = match.group(1)  # IP-адрес клиента
        client_id = match.group(2)   # идентификатор клиента
        user_id = match.group(3)     # имя пользователя
        timestamp = match.group(4)   # время запроса
        method = match.group(5)      # HTTP-метод (GET, POST)
        url = match.group(6)         # запрашиваемый URL
        protocol = match.group(7)    # версия протокола
        status_code = match.group(8) # код ответа
        size = match.group(9)        # размер ответа
        
        # Возвращаем словарь с разобранными данными
        return {
            'type': 'apache',  # тип лога
            'ip': ip_address,
            'timestamp': timestamp,
            'method': method,
            'url': url,
            'status': status_code,
            'size': size,
            'raw': log_line  # оригинальная строка
        }
    
    # Если строка не соответствует шаблону
    return None

def parse_nginx_log(log_line):
    """
    Парсит одну строку лога Nginx
    """
    # Более простой парсинг для Nginx
    parts = log_line.split()  # разбиваем строку на части по пробелам
    
    # Проверяем, достаточно ли частей в строке
    if len(parts) >= 7:
        # Создаем словарь с данными
        log_data = {
            'type': 'nginx',  # тип лога
            'ip': parts[0],   # первый элемент - IP-адрес
            'timestamp': ' '.join(parts[3:5]),  # время из 3 и 4 элемента
            'method': parts[5],  # метод запроса
            'url': parts[6],     # URL запроса
            'status': parts[8] if len(parts) > 8 else '000',  # код ответа
            'raw': log_line      # оригинальная строка
        }
        return log_data
    
    return None

def parse_syslog(log_line):
    """
    Парсит системный лог
    """
    # Ищем дату в начале строки
    date_pattern = r'(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})'
    
    # Пытаемся найти дату
    date_match = re.match(date_pattern, log_line)
    
    if date_match:
        # Извлекаем дату
        timestamp = date_match.group(1)
        
        # Разделяем оставшуюся часть строки
        rest = log_line[len(timestamp):].strip()
        parts = rest.split(maxsplit=2)  # разбиваем на 3 части
        
        # Проверяем, достаточно ли частей
        if len(parts) >= 3:
            return {
                'type': 'syslog',  # тип лога
                'timestamp': timestamp,  # временная метка
                'hostname': parts[0],    # имя хоста
                'process': parts[1],     # имя процесса
                'message': parts[2],     # сообщение
                'raw': log_line          # оригинальная строка
            }
    
    return None

def parse_log_file(file_path, log_type='auto'):
    """
    Читает и парсит весь файл логов
    """
    logs = []  # создаем пустой список для хранения логов
    
    try:
        # Открываем файл для чтения
        with open(file_path, 'r', encoding='utf-8') as file:
            # Читаем все строки из файла
            lines = file.readlines()
            
            # Проходим по каждой строке
            for line in lines:
                line = line.strip()  # удаляем лишние пробелы
                
                # Пропускаем пустые строки
                if not line:
                    continue
                
                parsed_log = None  # переменная для разобранного лога
                
                # Определяем тип лога автоматически
                if log_type == 'auto':
                    # Пробуем разные парсеры
                    parsed_log = parse_apache_log(line)
                    if not parsed_log:
                        parsed_log = parse_nginx_log(line)
                    if not parsed_log:
                        parsed_log = parse_syslog(line)
                elif log_type == 'apache':
                    parsed_log = parse_apache_log(line)
                elif log_type == 'nginx':
                    parsed_log = parse_nginx_log(line)
                elif log_type == 'syslog':
                    parsed_log = parse_syslog(line)
                
                # Если лог разобран успешно, добавляем в список
                if parsed_log:
                    logs.append(parsed_log)
                else:
                    # Если не удалось разобрать, сохраняем как сырой текст
                    logs.append({
                        'type': 'unknown',
                        'raw': line,
                        'message': line
                    })
    
    except FileNotFoundError:
        # Если файл не найден
        print(f"Ошибка: Файл {file_path} не найден!")
        return []
    except Exception as e:
        # Если произошла другая ошибка
        print(f"Ошибка при чтении файла: {e}")
        return []
    
    # Возвращаем список всех разобранных логов
    return logs