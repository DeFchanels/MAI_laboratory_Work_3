import re
from dataclasses import dataclass
from datetime import date

from .errors import BrokenDataError, InvalidEntityError


@dataclass
class MediaItem: # Класс для события
    id: str
    name: str
    category: str
    year: int
    resolution: str
    duration: int = 0  # Длительность в секундах, по дефолту (если фотография например) длительность 0

    def __post_init__(self):
        object.__setattr__(self, "resolution", self.resolution.strip())
        self.validate()

    def validate(self):
        non_durational_categories = ['photo', 'фото']
        resolution_pattern = r'^\d+\s*[xXхХ*]\s*\d+$'
        resolutions_shorts = ['SD', 'HD', 'Full HD', 'FULL HD', '2K', '4K', 'sd', 'hd', 'full hd', '2k', '4k', '8k', '8K']
        resolution = self.resolution
        year = self.year

        for name in ("id", "name", "category", "resolution"): # Проходим по атрибутам медиа
            value = getattr(self, name) # Получаем значение конкретного атрибута
            if not isinstance(value, str):
                raise InvalidEntityError(f"Field {name!r} must be str type")
            if not value.strip(): # Если значение пустое, возвращаем ошибку с соответсвующим сообщением
                raise InvalidEntityError(f"{name} cannot be empty")

        if not isinstance(year, int) or isinstance(year, bool): # Если год является нецелым числом
            raise InvalidEntityError("Year must be an integer")

        if not (0 <= year <= date.today().year): # Если введен невозможный год
            raise InvalidEntityError(f"Invalid year: {year}")

        if not bool(re.match(resolution_pattern, resolution)) and not (resolution in resolutions_shorts): # Проверка валидности разрешения
            raise InvalidEntityError(f'Invalid resolution format: {resolution}')

        if not isinstance(self.duration, int) or isinstance(self.duration, bool): # Если тип введенной длительности не совпадает с требуемым int
            raise InvalidEntityError("Duration must be an integer")

        if self.duration < 0: # Если длительность меньше 0
            raise InvalidEntityError("Duration must be positive")

        if self.category not in non_durational_categories and self.duration == 0: # Если объект должен иметь длительность, но она не введена или меньше (равна) 0
            raise InvalidEntityError(f"Duration for {self.category} must be > 0. Your duration: {self.duration}")

        if self.category in non_durational_categories and self.duration != 0: # Если объект не должен иметь длительность, но она отличается от 0, возвращаем ошибку
            raise InvalidEntityError(f"Duration for {self.category} must be = 0. Your duration: {self.duration}")


    def to_dict(self): # Возвращаем словарь аттрибутов
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "year": self.year,
            "resolution": self.resolution,
            "duration": self.duration,
        }

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                id=data["id"],
                name=data["name"],
                category=data["category"],
                year=data["year"],
                resolution=data["resolution"],
                duration=data.get("duration", 0)
            )
        except KeyError as e:
            raise BrokenDataError(f'Field {e.args[0]} is required')