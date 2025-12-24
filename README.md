# Модульные тесты для анализатора мультимедийных файлов

Этот проект содержит модульные тесты для программы анализатора мультимедийных файлов из практической работы 3.

## Структура проекта

```
tests/
├── README.md              # Этот файл
├── requirements.txt        # Зависимости для тестов
├── .gitignore             # Игнорируемые файлы
├── test_format_duration.py # Тесты для функции format_duration
├── test_get_file_info.py   # Тесты для функции get_file_info
├── test_detect_file_type.py # Тесты для функции detect_file_type
├── test_analyze_audio.py   # Тесты для функции analyze_audio
├── test_analyze_video.py   # Тесты для функции analyze_video
├── test_analyze_image.py   # Тесты для функции analyze_image
└── test_exceptions.py      # Тесты для исключительных ситуаций
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск конкретного теста
pytest test_format_duration.py

# Запуск с покрытием кода
pytest --cov=../multimedia_analyzer --cov-report=html
```

## Требования

- Python 3.8+
- pytest
- Все зависимости из основного проекта (tinytag, opencv-python, Pillow)

