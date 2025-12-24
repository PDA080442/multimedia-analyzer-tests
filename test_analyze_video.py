"""
Тесты для функции analyze_video
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import analyze_video


class TestAnalyzeVideo:
    """Тесты для функции analyze_video"""

    def test_analyze_video_valid_file(self, capsys):
        """Тест: анализ валидного видеофайла (проверка что функция выполняется без ошибок)"""
        # Создаем временный файл с расширением .mp4
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            tmp_file.write(b"fake video content")
            tmp_path = tmp_file.name
        
        try:
            # Функция может выдать ошибку при открытии, но не должна упасть
            analyze_video(tmp_path)
            captured = capsys.readouterr()
            # Проверяем, что функция вывела заголовок
            assert "АНАЛИЗ ВИДЕОФАЙЛА" in captured.out
            assert "Название файла:" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_analyze_video_file_not_found(self, capsys):
        """Тест: обработка ошибки при отсутствии файла"""
        non_existent_file = "/nonexistent/path/to/file.mp4"
        
        # Функция должна обработать ошибку и вывести информацию
        analyze_video(non_existent_file)
        captured = capsys.readouterr()
        # Должна быть ошибка при попытке получить информацию о файле
        assert "АНАЛИЗ ВИДЕОФАЙЛА" in captured.out

    def test_analyze_video_invalid_format(self, capsys):
        """Тест: обработка невалидного формата файла"""
        # Создаем файл с расширением .mp4, но с невалидным содержимым
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            tmp_file.write(b"not a real video file content")
            tmp_path = tmp_file.name
        
        try:
            analyze_video(tmp_path)
            captured = capsys.readouterr()
            # Функция должна обработать ошибку открытия
            assert "АНАЛИЗ ВИДЕОФАЙЛА" in captured.out
            assert "Название файла:" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_analyze_video_output_structure(self, capsys):
        """Тест: проверка структуры вывода функции"""
        with tempfile.NamedTemporaryFile(suffix=".avi", delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_path = tmp_file.name
        
        try:
            analyze_video(tmp_path)
            captured = capsys.readouterr()
            output = captured.out
            
            # Проверяем наличие основных элементов вывода
            assert "=" * 60 in output  # Разделитель
            assert "АНАЛИЗ ВИДЕОФАЙЛА" in output
            assert "Название файла:" in output
            assert "Размер файла:" in output
            assert "Дата последнего изменения:" in output
        finally:
            Path(tmp_path).unlink()

    def test_analyze_video_different_formats(self, capsys):
        """Тест: анализ файлов с разными расширениями"""
        formats = [".mp4", ".avi", ".mkv", ".mov", ".webm"]
        
        for ext in formats:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
                tmp_file.write(b"test content")
                tmp_path = tmp_file.name
            
            try:
                analyze_video(tmp_path)
                captured = capsys.readouterr()
                assert "АНАЛИЗ ВИДЕОФАЙЛА" in captured.out
            finally:
                Path(tmp_path).unlink()

