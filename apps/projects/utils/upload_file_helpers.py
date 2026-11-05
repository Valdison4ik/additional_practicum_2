import os
from pathlib import Path

""""
НЕ ИСПОЛЬЗУЕТСЯ В ПРОЕКТЕ из-за неработоспособности 
"""


ALLOWED_EXTENSIONS = ['.csv', '.doc', '.pdf', '.xlsx', '.py']


def check_extension(filename):
    """ Функция на проверку валидных расширений файла """
    extension = Path(filename).suffix
    if extension not in ALLOWED_EXTENSIONS:
        return False
    return True


def check_file_size(file, required_size=2):
    """Функция на проверку размерности файла (файл не должен быть больше 2 MB)"""
    file_size = file.size / (1024 * 1024)
    if file_size > required_size:
        return False
    return True

def create_file_path(file_name):
    """Функция на создание пути для сохранения файла"""
    new_file_name, file_ext = file_name.split('.')
    file_path = "documents/{}.{}".format(new_file_name, file_ext)
    return file_path


def save_file(file_path, file_content):
    """Функция на сохранение файла
    (файл должен записываться по частям для избежания
    потенциальных ошибок и потери данных)"""
    os.makedirs(os.path.dirname('documents/'), exist_ok=True)
    with open(file_path, 'wb') as f:
        for chunk in file_content.chunks():
            f.write(chunk)
    return file_path




""" методы из сериалайзера с вызовами этих функций
работать оно не научилось
"""
    # def validate_file_name(self, value: str) -> str:
    #     if not value.isascii():
    #         raise ValidationError("Please, provide a valid file name.")
    #
    #     if not check_extension(value):
    #         raise ValidationError("Valid file extensions: ['.csv', '.doc', '.pdf','.xlsx']")
    #
    #     return value

    # def create(self, validated_data):
    #     file_path = create_file_path(file_name=validated_data['name'])
    #
    #     raw_file = self.context.get('raw_file')
    #
    #     if check_file_size(file=raw_file):
    #         save_file(file_path=file_path, file_content=raw_file)
    #         validated_data['data_file'] = file_path
    #         return ProjectFile.objects.create(**validated_data)
    #     else:
    #         raise ValidationError("File size is too large (2 MB as maximum).")