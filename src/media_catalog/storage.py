import json

from .errors import BrokenDataError, UnsupportedFormatVersionError
from .media_catalog import MediaCatalog
from .media_item import MediaItem

FORMAT_VERSION = 1


def save(catalog, file_path): # Сохранение каталога в файл
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            catalog_data = [media.to_dict() for media in catalog]
            data_to_save = {
                "format_version": FORMAT_VERSION,
                "items": catalog_data,
            }
            json.dump(data_to_save, f)
    except FileNotFoundError:
        raise BrokenDataError(f"File not found: {file_path}")


def get_load(file_path): # Функция для получения каталога из файла
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            document = json.load(f)

        format_version = document.get("format_version")
        if format_version != FORMAT_VERSION:
            raise UnsupportedFormatVersionError(f"Версия формата {format_version} не поддерживается")

        if not isinstance(document["items"], list):
            raise BrokenDataError("Поле items должно быть типа list")

        new_catalog = MediaCatalog()
        for item in document["items"]:
            new_catalog.add(MediaItem.from_dict(item))
        return new_catalog
    except json.JSONDecodeError as exc:  # Ошибка чтения json
        raise BrokenDataError(f"Invalid JSON: {exc}")
    except FileNotFoundError:
        raise BrokenDataError(f"File not found: {file_path}")


def load(catalog, file_path): # Функция, получающая новый каталог из файла и загружающая его в ваш каталог, заменяя его
    new_catalog = get_load(file_path)
    catalog.replace_catalog(new_catalog)


def load_with_edit(catalog, file_path):
    new_catalog = get_load(file_path)
    catalog.merge_with(new_catalog)

