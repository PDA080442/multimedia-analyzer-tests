"""
Тесты для класса AudioFile
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import AudioFile


class TestAudioFile:
    """Тесты для класса AudioFile"""

    def test_audio_file_creation(self):
        """Тест: создание объекта AudioFile"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"fake mp3 content")
            tmp_path = tmp_file.name
        
        try:
            audio_file = AudioFile(tmp_path)
            assert audio_file.file_type == "audio"
            assert audio_file.name == Path(tmp_path).name
            # Метаданные могут быть None если файл невалидный
            assert hasattr(audio_file, 'bitrate')
            assert hasattr(audio_file, 'duration')
        finally:
            Path(tmp_path).unlink()

    def test_audio_file_wrong_type(self):
        """Тест: попытка создать AudioFile из файла неправильного типа"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(b"fake image")
            tmp_path = tmp_file.name
        
        try:
            with pytest.raises(ValueError, match="не является аудиофайлом"):
                AudioFile(tmp_path)
        finally:
            Path(tmp_path).unlink()

    def test_audio_file_str(self):
        """Тест: строковое представление AudioFile"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"test")
            tmp_path = tmp_file.name
        
        try:
            audio_file = AudioFile(tmp_path)
            str_repr = str(audio_file)
            assert "Аудио:" in str_repr
            assert audio_file.name in str_repr
            assert "Длительность:" in str_repr
            assert "Битрейт:" in str_repr
        finally:
            Path(tmp_path).unlink()

    def test_audio_file_load_metadata_failure(self):
        """Тест: загрузка метаданных при невалидном файле"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"not a real mp3 file")
            tmp_path = tmp_file.name
        
        try:
            audio_file = AudioFile(tmp_path)
            # Файл создается, но метаданные могут быть None
            assert audio_file.file_type == "audio"
            # Проверяем, что объект создан, даже если метаданные не загружены
            assert hasattr(audio_file, 'bitrate')
        finally:
            Path(tmp_path).unlink()

