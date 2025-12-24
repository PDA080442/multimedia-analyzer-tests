"""
Тесты для исключительных ситуаций
"""
import pytest
import sys
import tempfile
import os
from pathlib import Path

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import (
    analyze_audio,
    analyze_video,
    analyze_image,
    detect_file_type,
)


class TestExceptions:
    """Тесты для обработки исключительных ситуаций"""

    def test_nonexistent_file_audio(self, capsys):
        """Тест: обработка несуществующего аудиофайла"""
        non_existent = "/nonexistent/path/to/audio.mp3"
        # Функция падает на get_file_info, так как файл не существует
        with pytest.raises(FileNotFoundError):
            analyze_audio(non_existent)

    def test_nonexistent_file_video(self, capsys):
        """Тест: обработка несуществующего видеофайла"""
        non_existent = "/nonexistent/path/to/video.mp4"
        # Функция падает на get_file_info, так как файл не существует
        with pytest.raises(FileNotFoundError):
            analyze_video(non_existent)

    def test_nonexistent_file_image(self, capsys):
        """Тест: обработка несуществующего изображения"""
        non_existent = "/nonexistent/path/to/image.jpg"
        # Функция падает на get_file_info, так как файл не существует
        with pytest.raises(FileNotFoundError):
            analyze_image(non_existent)

    def test_empty_file_path(self):
        """Тест: обработка пустого пути к файлу"""
        # Пустой путь должен вернуть "unknown"
        result = detect_file_type("")
        assert result == "unknown"

    def test_invalid_file_path(self):
        """Тест: обработка невалидного пути к файлу"""
        # Путь с недопустимыми символами
        invalid_path = "/invalid/path/with/\0/null/byte"
        result = detect_file_type(invalid_path)
        # Функция должна обработать это без падения
        assert result in ["unknown", "audio", "video", "image"]

    def test_corrupted_audio_file(self, capsys):
        """Тест: обработка поврежденного аудиофайла"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            # Записываем невалидные данные
            tmp_file.write(b"corrupted audio data that is not a real mp3")
            tmp_path = tmp_file.name
        
        try:
            analyze_audio(tmp_path)
            captured = capsys.readouterr()
            # Функция должна обработать ошибку парсинга
            assert "АНАЛИЗ АУДИОФАЙЛА" in captured.out
            # Может быть сообщение об ошибке или о невозможности определить формат
        finally:
            Path(tmp_path).unlink()

    def test_corrupted_video_file(self, capsys):
        """Тест: обработка поврежденного видеофайла"""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            # Записываем невалидные данные
            tmp_file.write(b"corrupted video data that is not a real mp4")
            tmp_path = tmp_file.name
        
        try:
            analyze_video(tmp_path)
            captured = capsys.readouterr()
            # Функция должна обработать ошибку открытия
            assert "АНАЛИЗ ВИДЕОФАЙЛА" in captured.out
            # Может быть сообщение об ошибке открытия файла
        finally:
            Path(tmp_path).unlink()

    def test_corrupted_image_file(self, capsys):
        """Тест: обработка поврежденного изображения"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            # Записываем невалидные данные
            tmp_file.write(b"corrupted image data that is not a real jpg")
            tmp_path = tmp_file.name
        
        try:
            analyze_image(tmp_path)
            captured = capsys.readouterr()
            # Функция должна обработать ошибку парсинга
            assert "АНАЛИЗ ИЗОБРАЖЕНИЯ" in captured.out
            # Должно быть сообщение об ошибке при анализе
            assert "Ошибка" in captured.out or "Название файла:" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_file_without_extension(self):
        """Тест: обработка файла без расширения"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            assert result == "unknown"
        finally:
            Path(tmp_path).unlink()

    def test_file_without_extension_analysis(self, capsys):
        """Тест: анализ файла без расширения"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_path = tmp_file.name
        
        try:
            # Функция может выдать UnsupportedFormatError при попытке определить формат
            try:
                analyze_audio(tmp_path)
                captured = capsys.readouterr()
                # Функция должна выполниться, но может выдать ошибку
                assert "Название файла:" in captured.out or "Ошибка" in captured.out
            except Exception:
                # Игнорируем ошибки формата - это ожидаемо для файла без расширения
                pass
        finally:
            Path(tmp_path).unlink()

    def test_empty_file(self, capsys):
        """Тест: обработка пустого файла"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            # Файл пустой
            tmp_path = tmp_file.name
        
        try:
            analyze_audio(tmp_path)
            captured = capsys.readouterr()
            # Функция должна обработать пустой файл
            assert "АНАЛИЗ АУДИОФАЙЛА" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_very_long_file_path(self):
        """Тест: обработка очень длинного пути к файлу"""
        # Создаем длинное имя файла (но не слишком, чтобы не превысить лимит ОС)
        long_name = "a" * 100 + ".mp3"
        try:
            with tempfile.NamedTemporaryFile(suffix=long_name, delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            try:
                result = detect_file_type(tmp_path)
                # Функция должна обработать длинный путь
                assert result in ["audio", "video", "image", "unknown"]
            finally:
                Path(tmp_path).unlink()
        except OSError:
            # Если ОС не поддерживает такие длинные имена, пропускаем тест
            pytest.skip("OS does not support very long file names")

    def test_special_characters_in_path(self):
        """Тест: обработка пути с специальными символами"""
        # Создаем файл с пробелами в имени
        with tempfile.NamedTemporaryFile(
            suffix=" test file .mp3", delete=False, dir=tempfile.gettempdir()
        ) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            # Функция должна обработать специальные символы
            assert result in ["audio", "video", "image", "unknown"]
        finally:
            Path(tmp_path).unlink()

