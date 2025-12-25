"""
Тесты для класса MultimediaFile
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import MultimediaFile


class TestMultimediaFile:
    """Тесты для базового класса MultimediaFile"""

    def test_multimedia_file_creation(self):
        """Тест: создание объекта MultimediaFile"""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_path = tmp_file.name
        
        try:
            file_obj = MultimediaFile(tmp_path)
            assert file_obj.file_path == tmp_path
            assert file_obj.name == Path(tmp_path).name
            assert file_obj.size > 0
            assert file_obj.modified is not None
            assert file_obj.file_type == "unknown"  # .txt не входит в известные типы
        finally:
            Path(tmp_path).unlink()

    def test_multimedia_file_nonexistent(self):
        """Тест: попытка создать MultimediaFile из несуществующего файла"""
        with pytest.raises(FileNotFoundError):
            MultimediaFile("/nonexistent/path/to/file.txt")

    def test_multimedia_file_detect_audio_type(self):
        """Тест: определение типа аудиофайла"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"fake mp3")
            tmp_path = tmp_file.name
        
        try:
            file_obj = MultimediaFile(tmp_path)
            assert file_obj.file_type == "audio"
        finally:
            Path(tmp_path).unlink()

    def test_multimedia_file_detect_video_type(self):
        """Тест: определение типа видеофайла"""
        with tempfile.NamedTemporaryFile(suffix=".avi", delete=False) as tmp_file:
            tmp_file.write(b"fake video")
            tmp_path = tmp_file.name
        
        try:
            file_obj = MultimediaFile(tmp_path)
            assert file_obj.file_type == "video"
        finally:
            Path(tmp_path).unlink()

    def test_multimedia_file_detect_image_type(self):
        """Тест: определение типа изображения"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(b"fake image")
            tmp_path = tmp_file.name
        
        try:
            file_obj = MultimediaFile(tmp_path)
            assert file_obj.file_type == "image"
        finally:
            Path(tmp_path).unlink()

    def test_multimedia_file_str(self):
        """Тест: строковое представление объекта"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"test")
            tmp_path = tmp_file.name
        
        try:
            file_obj = MultimediaFile(tmp_path)
            str_repr = str(file_obj)
            assert file_obj.name in str_repr
            assert "audio" in str_repr or file_obj.file_type in str_repr
        finally:
            Path(tmp_path).unlink()

    def test_multimedia_file_repr(self):
        """Тест: представление объекта для отладки"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"test")
            tmp_path = tmp_file.name
        
        try:
            file_obj = MultimediaFile(tmp_path)
            repr_str = repr(file_obj)
            assert "MultimediaFile" in repr_str
            assert tmp_path in repr_str
        finally:
            Path(tmp_path).unlink()

