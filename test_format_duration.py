"""
Тесты для функции format_duration
"""
import pytest
import sys
from pathlib import Path

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import format_duration


class TestFormatDuration:
    """Тесты для функции format_duration"""

    def test_format_duration_none(self):
        """Тест: format_duration с None возвращает 'Неизвестно'"""
        result = format_duration(None)
        assert result == "Неизвестно"

    def test_format_duration_seconds_only(self):
        """Тест: форматирование только секунд (менее минуты)"""
        result = format_duration(45)
        assert result == "00:45"
        
        result = format_duration(5)
        assert result == "00:05"
        
        result = format_duration(0)
        assert result == "00:00"

    def test_format_duration_minutes_seconds(self):
        """Тест: форматирование минут и секунд"""
        result = format_duration(125)  # 2 минуты 5 секунд
        assert result == "02:05"
        
        result = format_duration(3599)  # 59 минут 59 секунд
        assert result == "59:59"
        
        result = format_duration(60)  # 1 минута
        assert result == "01:00"

    def test_format_duration_hours_minutes_seconds(self):
        """Тест: форматирование часов, минут и секунд"""
        result = format_duration(3661)  # 1 час 1 минута 1 секунда
        assert result == "01:01:01"
        
        result = format_duration(7323)  # 2 часа 2 минуты 3 секунды
        assert result == "02:02:03"
        
        result = format_duration(3600)  # 1 час
        assert result == "01:00:00"

    def test_format_duration_zero(self):
        """Тест: форматирование нулевого значения"""
        result = format_duration(0)
        assert result == "00:00"
        
    def test_format_duration_float(self):
        """Тест: форматирование дробных значений"""
        result = format_duration(125.7)  # Дробная часть отбрасывается
        assert result == "02:05"
        
        result = format_duration(3661.9)
        assert result == "01:01:01"

