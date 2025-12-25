# test.py
print("Тест импортов...")
try:
    import config
    print("config импортирован успешно")
    
    from log_parser import parse_apache_log
    print("log_parser импортирован успешно")
    
    print("Все импорты работают!")
except ImportError as e:
    print(f"Ошибка импорта: {e}")