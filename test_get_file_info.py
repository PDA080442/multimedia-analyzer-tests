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
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_path = tmp_file.name
        
        try:
            info = get_file_info(tmp_path)
            assert "name" in info
            assert "size" in info
            assert "modified" in info
            assert isinstance(info["name"], str)
            assert isinstance(info["size"], int)
            assert isinstance(info["modified"], str)
        finally:
            os.unlink(tmp_path)

    def test_get_file_info_file_name(self):
        """Тест: проверка правильности имени файла"""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp_file:
            tmp_file.write(b"test")
            tmp_path = tmp_file.name
        
        try:
            info = get_file_info(tmp_path)
            expected_name = Path(tmp_path).name
            assert info["name"] == expected_name
        finally:
            os.unlink(tmp_path)

    def test_get_file_info_file_size(self):
        """Тест: проверка правильности размера файла"""
        test_content = b"test content for size check"
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(test_content)
            tmp_path = tmp_file.name
        
        try:
            info = get_file_info(tmp_path)
            assert info["size"] == len(test_content)
            assert info["size"] > 0
        finally:
            os.unlink(tmp_path)

    def test_get_file_info_modified_time(self):
        """Тест: проверка формата времени модификации"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"test")
            tmp_path = tmp_file.name
        
        try:
            info = get_file_info(tmp_path)
            # Проверяем формат: YYYY-MM-DD HH:MM:SS
            assert len(info["modified"]) == 19
            assert info["modified"][4] == "-"  # Разделитель года
            assert info["modified"][7] == "-"  # Разделитель месяца
            assert info["modified"][10] == " "  # Разделитель даты и времени
            assert info["modified"][13] == ":"  # Разделитель часов
            assert info["modified"][16] == ":"  # Разделитель минут
        finally:
            os.unlink(tmp_path)

