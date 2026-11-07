from .errors import InvalidEntityError, IdError, NotFoundError
from .media_item import MediaItem


class MediaCatalog: # Класс для каталога медиа
    def __init__(self):
        self.items: dict[str, MediaItem] = {}
        self.order_list: list[str] = []
        self.item_ids_by_category: dict[str, list[str]] = {}

    def replace_catalog(self, other_catalog):
        self.items = dict(other_catalog.items)
        self.order_list = list(other_catalog.order_list)
        self.item_ids_by_category = {category: list(items) for category, items in other_catalog.item_ids_by_category.items()}

    def merge_with(self, other_catalog):
        for item in other_catalog:
            try:
                self.add(item)
            except IdError:
                self.remove(item.id)
                self.add(item)

    def add(self, item): # Добавление элемента в каталог
        if not isinstance(item, MediaItem): # Если тип добавляемого элемента отличается от необходимого MediaItem
            raise InvalidEntityError('Element for catalog must be of type MediaItem')

        if item.id in self.items: # Если id добавляемого элемента уже находится в каталоге, возвращаем ошибку
            raise IdError(f"Id {item.id} already exists in catalog")

        self.items[item.id] = item # Сохраняем элемент в каталог
        self.order_list.append(item.id) # Сохраняем id элемента в список, чтобы потом знать порядок добавления элементов

        if item.category not in self.item_ids_by_category: #  Добавляем элемент в список, соответствующий его категории
            self.item_ids_by_category[item.category] = [item.id]
        else:
            self.item_ids_by_category[item.category].append(item.id)

    def remove(self, item_id): # Удаление элемента из каталога
        item = self.items.pop(item_id, None)
        if item is None:  # Если пытаемся удалить элемент, которого нет в каталоге
            raise NotFoundError(f"Id {item_id} doesn't exist in catalog")
        self.order_list.remove(item_id) # Удаляем id из списка
        self.item_ids_by_category[item.category].remove(item.id)
        if not self.item_ids_by_category[item.category]: # Если элемент был единственный в категории, стираем эту категорию из ключей
            del self.item_ids_by_category[item.category]

    def get(self, item_id): # Получение элемента из каталога
        try:
            return self.items[item_id]
        except KeyError:
            raise NotFoundError(f"Id {item_id} doesn't exists in catalog")

    def find_by_category(self, category):
        return [self.items[i] for i in self.item_ids_by_category.get(category, [])]

    def find_by_name(self, name):
        return [self.items[i] for i in self.order_list if self.items[i].name.lower() == name.lower()]

    def __len__(self):
        return len(self.items)

    def  __iter__(self):
        for item_id in self.order_list:
            yield self.items[item_id]

    def __contains__(self, item_id):
        return item_id in self.items

