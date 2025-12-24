"""
Тесты для функции detect_file_type
"""
import pytest
import sys
from pathlib import Path
import tempfile

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import detect_file_type


class TestDetectFileType:
    """Тесты для функции detect_file_type"""

    def test_detect_audio_mp3(self):
        """Тест: определение MP3 как аудио"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            assert result == "audio"
        finally:
            Path(tmp_path).unlink()

    def test_detect_audio_wav(self):
        """Тест: определение WAV как аудио"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            assert result == "audio"
        finally:
            Path(tmp_path).unlink()

    def test_detect_audio_other_formats(self):
        """Тест: определение других аудио форматов"""
        audio_formats = [".flac", ".m4a", ".aac", ".ogg", ".wma"]
        for ext in audio_formats:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            try:
                result = detect_file_type(tmp_path)
                assert result == "audio", f"Формат {ext} должен определяться как audio"
            finally:
                Path(tmp_path).unlink()

    def test_detect_video_mp4(self):
        """Тест: определение MP4 как видео (если это видео файл)"""
        # MP4 может быть и аудио, и видео - зависит от содержимого
        # Если файл не является валидным видео, вернется "audio"
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            # MP4 без видео контента вернет "audio"
            assert result in ["audio", "video"]
        finally:
            Path(tmp_path).unlink()

    def test_detect_video_avi(self):
        """Тест: определение AVI как видео"""
        with tempfile.NamedTemporaryFile(suffix=".avi", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            assert result == "video"
        finally:
            Path(tmp_path).unlink()

    def test_detect_video_other_formats(self):
        """Тест: определение других видео форматов"""
        video_formats = [".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg"]
        for ext in video_formats:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            try:
                result = detect_file_type(tmp_path)
                assert result == "video", f"Формат {ext} должен определяться как video"
            finally:
                Path(tmp_path).unlink()

    def test_detect_image_jpg(self):
        """Тест: определение JPG как изображение"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            assert result == "image"
        finally:
            Path(tmp_path).unlink()

    def test_detect_image_png(self):
        """Тест: определение PNG как изображение"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            assert result == "image"
        finally:
            Path(tmp_path).unlink()

    def test_detect_image_other_formats(self):
        """Тест: определение других форматов изображений"""
        image_formats = [".jpeg", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg"]
        for ext in image_formats:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            try:
                result = detect_file_type(tmp_path)
                assert result == "image", f"Формат {ext} должен определяться как image"
            finally:
                Path(tmp_path).unlink()

    def test_detect_unknown_extension(self):
        """Тест: определение неизвестного расширения"""
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            assert result == "unknown"
        finally:
            Path(tmp_path).unlink()

    def test_detect_file_without_extension(self):
        """Тест: определение файла без расширения"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = detect_file_type(tmp_path)
            assert result == "unknown"
        finally:
            Path(tmp_path).unlink()

    def test_detect_case_insensitive(self):
        """Тест: определение типа файла независимо от регистра расширения"""
        # Тестируем разные регистры для одного формата
        test_cases = [
            (".MP3", "audio"),
            (".WAV", "audio"),
            (".JPG", "image"),
            (".PNG", "image"),
            (".AVI", "video"),
            (".MKV", "video"),
        ]
        
        for ext, expected_type in test_cases:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            try:
                result = detect_file_type(tmp_path)
                assert result == expected_type, \
                    f"Формат {ext} должен определяться как {expected_type}"
            finally:
                Path(tmp_path).unlink()

