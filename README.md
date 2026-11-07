# Каталог объектов «Медиатека»
#### Python-пакет `media_catalog`, позволяющий управлять медиатекой (фильмы, музыка, фото), выполнять поиск по категориям и сохранять данные в JSON.

## Скачивание и подготовка к использованию
1. Склонируйте или скачайте проект к себе
2. Создайте виртуальное окружение:
 - Введите в консоль команду `python -m venv .venv`.
 - Затем пропишите `.venv/bin/activate` (для Linux/macOS) или `.venv\Scripts\activate` (для Windows).
3. Установите зависимости:
 - `python -m pip install -r requirements.txt`

#### После этого пакет готов к использованию в вашем Python-коде.

## Использование и тестирование
1. Для использования каталога в вашем коде импортируйте классы из пакета. Пример базового сценария:
```python
from src.media_catalog.media_item import MediaItem
from src.media_catalog.media_catalog import MediaCatalog
from src.media_catalog.storage import save, load

# Создаем элемент (если duration не указан для фото, по умолчанию будет 0)
item = MediaItem(id="1", name="Матрица", category="фильм", year=1999, resolution="1920x1080", duration=9000)

# Добавляем в каталог
catalog = MediaCatalog()
catalog.add(item)

# Сохраняем в JSON (автоматически добавится format_version)
save(catalog, "my_catalog.json")

# Загружаем обратно
new_catalog = MediaCatalog()
load(new_catalog, "my_catalog.json")