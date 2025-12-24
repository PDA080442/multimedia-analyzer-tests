"""
Тесты для функции get_file_info
"""
import pytest
import sys
from pathlib import Path
import tempfile
import os

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import get_file_info


class TestGetFileInfo:
    """Тесты для функции get_file_info"""

    def test_get_file_info_existing_file(self):
        """Тест: получение информации о существующем файле"""
        # TODO: Реализовать тест
        pass

    def test_get_file_info_file_name(self):
        """Тест: проверка правильности имени файла"""
        # TODO: Реализовать тест
        pass

    def test_get_file_info_file_size(self):
        """Тест: проверка правильности размера файла"""
        # TODO: Реализовать тест
        pass

    def test_get_file_info_modified_time(self):
        """Тест: проверка формата времени модификации"""
        # TODO: Реализовать тест
        pass

