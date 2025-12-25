"""
Тесты для функции process_commands
"""
import pytest
import sys
import tempfile
from pathlib import Path
from PIL import Image

# Добавляем путь к основному проекту для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from multimedia_analyzer import process_commands


class TestProcessCommands:
    """Тесты для функции process_commands"""

    def test_process_commands_nonexistent_file(self, capsys):
        """Тест: обработка несуществующего файла команд"""
        process_commands("/nonexistent/commands.txt")
        captured = capsys.readouterr()
        assert "Ошибка" in captured.out
        assert "не найден" in captured.out

    def test_process_commands_add_and_print(self, capsys):
        """Тест: команды ADD и PRINT"""
        # Создаем файл с командами
        with tempfile.NamedTemporaryFile(mode='w', suffix=".txt", delete=False) as cmd_file:
            cmd_file.write("ADD test_image.png\n")
            cmd_file.write("PRINT\n")
            cmd_path = cmd_file.name
        
        # Создаем тестовое изображение
        with tempfile.NamedTemporaryFile(suffix="test_image.png", delete=False) as img_file:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(img_file.name, 'PNG')
            img_path = img_file.name
        
        try:
            # Обновляем путь в файле команд на реальный путь
            with open(cmd_path, 'w') as f:
                f.write(f"ADD {img_path}\n")
                f.write("PRINT\n")
            
            process_commands(cmd_path)
            captured = capsys.readouterr()
            assert "Добавлен:" in captured.out
            assert "Содержимое контейнера" in captured.out or "Контейнер пуст" in captured.out
        finally:
            Path(cmd_path).unlink()
            Path(img_path).unlink()

    def test_process_commands_ignore_comments(self, capsys):
        """Тест: игнорирование комментариев"""
        with tempfile.NamedTemporaryFile(mode='w', suffix=".txt", delete=False) as cmd_file:
            cmd_file.write("# Это комментарий\n")
            cmd_file.write("  # Еще один комментарий\n")
            cmd_file.write("\n")  # Пустая строка
            cmd_file.write("PRINT\n")
            cmd_path = cmd_file.name
        
        try:
            process_commands(cmd_path)
            captured = capsys.readouterr()
            # Комментарии не должны обрабатываться
            assert "Контейнер пуст" in captured.out
        finally:
            Path(cmd_path).unlink()

    def test_process_commands_add_error(self, capsys):
        """Тест: обработка ошибки при команде ADD"""
        with tempfile.NamedTemporaryFile(mode='w', suffix=".txt", delete=False) as cmd_file:
            cmd_file.write("ADD /nonexistent/file.mp3\n")
            cmd_file.write("PRINT\n")
            cmd_path = cmd_file.name
        
        try:
            process_commands(cmd_path)
            captured = capsys.readouterr()
            assert "Ошибка" in captured.out or "не найден" in captured.out
            assert "Контейнер пуст" in captured.out
        finally:
            Path(cmd_path).unlink()

    def test_process_commands_add_without_argument(self, capsys):
        """Тест: команда ADD без аргумента"""
        with tempfile.NamedTemporaryFile(mode='w', suffix=".txt", delete=False) as cmd_file:
            cmd_file.write("ADD\n")
            cmd_file.write("PRINT\n")
            cmd_path = cmd_file.name
        
        try:
            process_commands(cmd_path)
            captured = capsys.readouterr()
            assert "Ошибка" in captured.out or "требует аргумент" in captured.out
        finally:
            Path(cmd_path).unlink()

    def test_process_commands_rem_without_argument(self, capsys):
        """Тест: команда REM без аргумента"""
        with tempfile.NamedTemporaryFile(mode='w', suffix=".txt", delete=False) as cmd_file:
            cmd_file.write("REM\n")
            cmd_file.write("PRINT\n")
            cmd_path = cmd_file.name
        
        try:
            process_commands(cmd_path)
            captured = capsys.readouterr()
            assert "Ошибка" in captured.out or "требует аргумент" in captured.out
        finally:
            Path(cmd_path).unlink()

