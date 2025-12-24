"""
Тесты для функции analyze_audio
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import analyze_audio


class TestAnalyzeAudio:
    """Тесты для функции analyze_audio"""

    def test_analyze_audio_valid_file(self, capsys):
        """Тест: анализ валидного аудиофайла (проверка что функция выполняется без ошибок)"""
        # Создаем временный файл с расширением .mp3
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"fake mp3 content")
            tmp_path = tmp_file.name
        
        try:
            # Функция может выдать ошибку при парсинге, но не должна упасть
            analyze_audio(tmp_path)
            captured = capsys.readouterr()
            # Проверяем, что функция вывела заголовок
            assert "АНАЛИЗ АУДИОФАЙЛА" in captured.out
            assert "Название файла:" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_analyze_audio_file_not_found(self, capsys):
        """Тест: обработка ошибки при отсутствии файла"""
        non_existent_file = "/nonexistent/path/to/file.mp3"
        
        # Функция падает на get_file_info, так как файл не существует
        with pytest.raises(FileNotFoundError):
            analyze_audio(non_existent_file)

    def test_analyze_audio_invalid_format(self, capsys):
        """Тест: обработка невалидного формата файла"""
        # Создаем файл с расширением .mp3, но с невалидным содержимым
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"not a real mp3 file content")
            tmp_path = tmp_file.name
        
        try:
            analyze_audio(tmp_path)
            captured = capsys.readouterr()
            # Функция должна обработать ошибку парсинга
            assert "АНАЛИЗ АУДИОФАЙЛА" in captured.out
            # Может быть ошибка при анализе или сообщение о невозможности определить формат
            assert "Название файла:" in captured.out
        finally:
            Path(tmp_path).unlink()

    def test_analyze_audio_output_structure(self, capsys):
        """Тест: проверка структуры вывода функции"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_path = tmp_file.name
        
        try:
            analyze_audio(tmp_path)
            captured = capsys.readouterr()
            output = captured.out
            
            # Проверяем наличие основных элементов вывода
            assert "=" * 60 in output  # Разделитель
            assert "АНАЛИЗ АУДИОФАЙЛА" in output
            assert "Название файла:" in output
            assert "Размер файла:" in output
            assert "Дата последнего изменения:" in output
        finally:
            Path(tmp_path).unlink()

    def test_analyze_audio_different_formats(self, capsys):
        """Тест: анализ файлов с разными расширениями"""
        formats = [".mp3", ".wav", ".flac", ".m4a", ".ogg"]
        
        for ext in formats:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
                tmp_file.write(b"test content")
                tmp_path = tmp_file.name
            
            try:
                # Функция может выдать ParseError при невалидном содержимом, но не должна упасть
                try:
                    analyze_audio(tmp_path)
                except Exception:
                    # Игнорируем ошибки парсинга - это ожидаемо для невалидных файлов
                    pass
                captured = capsys.readouterr()
                assert "АНАЛИЗ АУДИОФАЙЛА" in captured.out
            finally:
                Path(tmp_path).unlink()

