class CatalogError(Exception):
    """Basic Exception"""


class InvalidEntityError(CatalogError):
    """Raised when an entity being created is invalid"""


class IdError(CatalogError):
    """Raised when an id is already existed"""


class NotFoundError(CatalogError):
    """Raised when an entity being got was not found"""


class UnsupportedFormatVersionError(CatalogError):
    """Неизвестная версия формата."""


class BrokenDataError(CatalogError):
    """Raised when an file from which entity is creating is corrupted"""