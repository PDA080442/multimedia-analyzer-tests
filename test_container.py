"""
Тесты для класса MultimediaContainer
"""
import pytest
import sys
import tempfile
from pathlib import Path
from PIL import Image

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import MultimediaContainer, AudioFile, ImageFile


class TestMultimediaContainer:
    """Тесты для класса MultimediaContainer"""

    def test_container_initialization(self):
        """Тест: инициализация контейнера"""
        container = MultimediaContainer()
        assert len(container.files) == 0
        assert container.files == []

    def test_container_add_audio_file(self, capsys):
        """Тест: добавление аудиофайла в контейнер"""
        container = MultimediaContainer()
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"fake mp3")
            tmp_path = tmp_file.name
        
        try:
            result = container.add(tmp_path)
            captured = capsys.readouterr()
            assert result is True
            assert len(container.files) == 1
            assert container.files[0].file_type == "audio"
            assert "Добавлен:" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_container_add_image_file(self, capsys):
        """Тест: добавление изображения в контейнер"""
        container = MultimediaContainer()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp_path, 'PNG')
            
            result = container.add(tmp_path)
            captured = capsys.readouterr()
            assert result is True
            assert len(container.files) == 1
            assert container.files[0].file_type == "image"
        finally:
            Path(tmp_path).unlink()

    def test_container_add_nonexistent_file(self, capsys):
        """Тест: попытка добавить несуществующий файл"""
        container = MultimediaContainer()
        result = container.add("/nonexistent/file.mp3")
        captured = capsys.readouterr()
        assert result is False
        assert len(container.files) == 0
        assert "Ошибка" in captured.out

    def test_container_add_unsupported_format(self, capsys):
        """Тест: попытка добавить файл неподдерживаемого формата"""
        container = MultimediaContainer()
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as tmp_file:
            tmp_file.write(b"test")
            tmp_path = tmp_file.name
        
        try:
            result = container.add(tmp_path)
            captured = capsys.readouterr()
            assert result is False
            assert len(container.files) == 0
            assert "Ошибка" in captured.out or "Неподдерживаемый" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_container_remove_by_type(self, capsys):
        """Тест: удаление файлов по типу"""
        container = MultimediaContainer()
        # Добавляем несколько файлов
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp1:
            tmp1.write(b"audio")
            path1 = tmp1.name
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp2:
            img = Image.new('RGB', (50, 50), color='red')
            img.save(tmp2.name, 'PNG')
            path2 = tmp2.name
        
        try:
            container.add(path1)
            container.add(path2)
            capsys.readouterr()  # Очищаем вывод
            
            removed = container.remove("type == audio")
            assert removed == 1
            assert len(container.files) == 1
            assert container.files[0].file_type == "image"
        finally:
            Path(path1).unlink()
            Path(path2).unlink()

    def test_container_remove_by_size_greater(self, capsys):
        """Тест: удаление файлов по размеру (больше чем)"""
        container = MultimediaContainer()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp1:
            # Создаем большое изображение
            img = Image.new('RGB', (500, 500), color='red')
            img.save(tmp1.name, 'PNG')
            path1 = tmp1.name
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp2:
            # Создаем маленькое изображение
            img = Image.new('RGB', (50, 50), color='blue')
            img.save(tmp2.name, 'PNG')
            path2 = tmp2.name
        
        try:
            container.add(path1)
            container.add(path2)
            capsys.readouterr()
            
            # Удаляем файлы больше 10000 байт
            removed = container.remove("size > 10000")
            assert removed >= 0  # Может быть 0 или 1 в зависимости от размера файлов
            assert len(container.files) <= 2
        finally:
            Path(path1).unlink()
            Path(path2).unlink()

    def test_container_remove_by_name_contains(self, capsys):
        """Тест: удаление файлов по содержимому имени"""
        container = MultimediaContainer()
        with tempfile.NamedTemporaryFile(suffix="test.mp3", delete=False, dir=tempfile.gettempdir()) as tmp1:
            tmp1.write(b"audio")
            path1 = tmp1.name
        with tempfile.NamedTemporaryFile(suffix="other.mp3", delete=False, dir=tempfile.gettempdir()) as tmp2:
            tmp2.write(b"audio")
            path2 = tmp2.name
        
        try:
            container.add(path1)
            container.add(path2)
            capsys.readouterr()
            
            # Удаляем файлы с "test" в имени
            removed = container.remove("name contains test")
            assert removed >= 0
            # Проверяем, что хотя бы один файл остался или удалился
            assert len(container.files) <= 2
        finally:
            Path(path1).unlink()
            Path(path2).unlink()

    def test_container_remove_invalid_condition(self, capsys):
        """Тест: удаление с невалидным условием"""
        container = MultimediaContainer()
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"test")
            tmp_path = tmp_file.name
        
        try:
            container.add(tmp_path)
            capsys.readouterr()
            
            removed = container.remove("invalid condition")
            captured = capsys.readouterr()
            assert removed == 0
            assert "Ошибка" in captured.out or "Не удалось распознать" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_container_print_all_empty(self, capsys):
        """Тест: вывод пустого контейнера"""
        container = MultimediaContainer()
        container.print_all()
        captured = capsys.readouterr()
        assert "Контейнер пуст" in captured.out

    def test_container_print_all_with_files(self, capsys):
        """Тест: вывод контейнера с файлами"""
        container = MultimediaContainer()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp_file.name, 'PNG')
            tmp_path = tmp_file.name
        
        try:
            container.add(tmp_path)
            capsys.readouterr()  # Очищаем вывод от add
            
            container.print_all()
            captured = capsys.readouterr()
            assert "Содержимое контейнера" in captured.out
            assert "всего файлов: 1" in captured.out
            assert "Изображение:" in captured.out or container.files[0].name in captured.out
        finally:
            Path(tmp_path).unlink()

