"""
Тесты для функции analyze_image
"""
import pytest
import sys
import tempfile
from pathlib import Path
from PIL import Image

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import analyze_image


class TestAnalyzeImage:
    """Тесты для функции analyze_image"""

    def test_analyze_image_valid_file(self, capsys):
        """Тест: анализ валидного изображения"""
        # Создаем реальное изображение для теста
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Создаем простое изображение
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp_path, 'PNG')
            
            analyze_image(tmp_path)
            captured = capsys.readouterr()
            output = captured.out
            
            # Проверяем наличие основных элементов вывода
            assert "АНАЛИЗ ИЗОБРАЖЕНИЯ" in output
            assert "Название файла:" in output
            assert "Размер файла:" in output
            assert "Разрешение:" in output
            assert "100 x 100" in output
            assert "Формат:" in output
            assert "PNG" in output
        finally:
            Path(tmp_path).unlink()

    def test_analyze_image_file_not_found(self, capsys):
        """Тест: обработка ошибки при отсутствии файла"""
        non_existent_file = "/nonexistent/path/to/file.jpg"
        
        # Функция должна обработать ошибку и вывести информацию
        analyze_image(non_existent_file)
        captured = capsys.readouterr()
        # Должна быть ошибка при попытке получить информацию о файле
        assert "АНАЛИЗ ИЗОБРАЖЕНИЯ" in captured.out

    def test_analyze_image_invalid_format(self, capsys):
        """Тест: обработка невалидного формата файла"""
        # Создаем файл с расширением .jpg, но с невалидным содержимым
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(b"not a real image file content")
            tmp_path = tmp_file.name
        
        try:
            analyze_image(tmp_path)
            captured = capsys.readouterr()
            # Функция должна обработать ошибку парсинга
            assert "АНАЛИЗ ИЗОБРАЖЕНИЯ" in captured.out
            assert "Название файла:" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_analyze_image_output_structure(self, capsys):
        """Тест: проверка структуры вывода функции"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Создаем простое изображение
            img = Image.new('RGB', (200, 150), color='blue')
            img.save(tmp_path, 'JPEG')
            
            analyze_image(tmp_path)
            captured = capsys.readouterr()
            output = captured.out
            
            # Проверяем наличие основных элементов вывода
            assert "=" * 60 in output  # Разделитель
            assert "АНАЛИЗ ИЗОБРАЖЕНИЯ" in output
            assert "Название файла:" in output
            assert "Размер файла:" in output
            assert "Дата последнего изменения:" in output
            assert "Разрешение:" in output
            assert "Цветовой режим:" in output
        finally:
            Path(tmp_path).unlink()

    def test_analyze_image_different_formats(self, capsys):
        """Тест: анализ файлов с разными форматами изображений"""
        formats = [('PNG', '.png'), ('JPEG', '.jpg'), ('GIF', '.gif')]
        
        for format_name, ext in formats:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            try:
                # Создаем изображение в соответствующем формате
                img = Image.new('RGB', (50, 50), color='green')
                img.save(tmp_path, format_name)
                
                analyze_image(tmp_path)
                captured = capsys.readouterr()
                assert "АНАЛИЗ ИЗОБРАЖЕНИЯ" in captured.out
            finally:
                Path(tmp_path).unlink()

    def test_analyze_image_rgb_mode(self, capsys):
        """Тест: проверка анализа RGB изображения"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp_path, 'PNG')
            
            analyze_image(tmp_path)
            captured = capsys.readouterr()
            output = captured.out
            
            assert "RGB" in output
            assert "Количество каналов: 3" in output
        finally:
            Path(tmp_path).unlink()

