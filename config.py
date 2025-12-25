# Настройки анализатора логов
ERROR_KEYWORDS = ['error', 'ERROR', 'Error', 'failed', 'Failed']
WARNING_KEYWORDS = ['warning', 'WARNING', 'Warning', 'warn']
# Типы логов, которые мы умеем парсить
LOG_TYPES = {
    'apache': 'Apache Web Server',  # логи Apache
    'nginx': 'Nginx Web Server',    # логи Nginx
    'syslog': 'System Log',         # системные логи
    'rsyslog': 'Rsyslog Daemon'     # демон rsyslog
}

# Уровни важности (приоритеты)
LOG_LEVELS = {
    'INFO': 1,      # информационные сообщения
    'WARNING': 2,   # предупреждения
    'ERROR': 3,     # ошибки
    'CRITICAL': 4   # критические ошибки
}

# Путь к файлу логов по умолчанию
DEFAULT_LOG_PATH = '/var/log/syslog'  # стандартный путь в Linux
