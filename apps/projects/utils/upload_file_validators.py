import os
from rest_framework.serializers import ValidationError

# Настройки ограничений (можно вынести в settings.py)
MAX_FILE_SIZE = 2 * 1024 * 1024  # 5 Мегабайт
ALLOWED_EXTENSIONS = ['.csv', '.doc', '.pdf', '.xlsx', '.py']


def validate_file_size(value):
    """Проверка максимального размера файла"""
    if value.size > MAX_FILE_SIZE:
        raise ValidationError(f"Файл слишком большой. Максимальный размер: {MAX_FILE_SIZE / (1024*1024)} МБ.")
    return value


def validate_file_extension(value):
    """Проверка расширения файла"""
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Неподдерживаемый формат файла. Разрешены только: {', '.join(ALLOWED_EXTENSIONS)}")
    return value