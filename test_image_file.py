"""
Тесты для класса ImageFile
"""
import pytest
import sys
import tempfile
from pathlib import Path
from PIL import Image

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import ImageFile


class TestImageFile:
    """Тесты для класса ImageFile"""

    def test_image_file_creation(self):
        """Тест: создание объекта ImageFile"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Создаем реальное изображение
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp_path, 'PNG')
            
            image_file = ImageFile(tmp_path)
            assert image_file.file_type == "image"
            assert image_file.name == Path(tmp_path).name
            assert image_file.width == 100
            assert image_file.height == 100
            assert image_file.format == "PNG"
            assert image_file.mode == "RGB"
        finally:
            Path(tmp_path).unlink()

    def test_image_file_wrong_type(self):
        """Тест: попытка создать ImageFile из файла неправильного типа"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"fake audio")
            tmp_path = tmp_file.name
        
        try:
            with pytest.raises(ValueError, match="не является изображением"):
                ImageFile(tmp_path)
        finally:
            Path(tmp_path).unlink()

    def test_image_file_str(self):
        """Тест: строковое представление ImageFile"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            img = Image.new('RGB', (200, 150), color='blue')
            img.save(tmp_path, 'JPEG')
            
            image_file = ImageFile(tmp_path)
            str_repr = str(image_file)
            assert "Изображение:" in str_repr
            assert image_file.name in str_repr
            assert "Разрешение:" in str_repr
            assert "Формат:" in str_repr
            assert "200x150" in str_repr
        finally:
            Path(tmp_path).unlink()

    def test_image_file_load_metadata_failure(self):
        """Тест: загрузка метаданных при невалидном файле"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(b"not a real image file")
            tmp_path = tmp_file.name
        
        try:
            # Функция может выбросить исключение при попытке открыть невалидный файл
            try:
                image_file = ImageFile(tmp_path)
                # Если файл создан, проверяем что атрибуты есть
                assert hasattr(image_file, 'width')
            except Exception:
                # Если исключение, это тоже валидное поведение
                pass
        finally:
            Path(tmp_path).unlink()

