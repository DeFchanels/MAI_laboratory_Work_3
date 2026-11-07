import pytest

from src.media_catalog.errors import BrokenDataError, InvalidEntityError
from src.media_catalog.media_item import MediaItem


def test_valid_item_created_1():
    data = {
        "id": "1",
        "name": "Матрица",
        "category": "фильм",
        "year": 1999,
        "resolution": "1920x1080",
        "duration": 9000,
    }
    item = MediaItem.from_dict(data)
    assert (item.id, item.name, item.category, item.year, item.resolution, item.duration) == ("1", "Матрица", "фильм", 1999, "1920x1080", 9000)

def test_valid_item_created_2():
    data = {
        "id": "1",
        "name": "Photo 1",
        "category": "photo",
        "year": 1890,
        "resolution": "HD",
        "duration": 0,
    }
    item = MediaItem.from_dict(data)
    assert (item.id, item.name, item.category, item.year, item.resolution, item.duration) == ("1", "Photo 1", "photo", 1890, "HD", 0)

def test_valid_item_created_3():
    data = {
        "id": "1",
        "name": "Photo 1",
        "category": "photo",
        "year": 1890,
        "resolution": "HD"
    }
    item = MediaItem.from_dict(data)
    assert (item.id, item.name, item.category, item.year, item.resolution, item.duration) == ("1", "Photo 1", "photo", 1890, "HD", 0)

def test_empty_task():
    data = {
        "id": "2",
        "name": "",
        "category": "photo",
        "year": 1890,
        "resolution": "HD",
        "duration": 0
    }
    with pytest.raises(InvalidEntityError):
        MediaItem.from_dict(data)

def test_invalid_resolution():
    data = {
        "id": "3",
        "name": "Photo 1",
        "category": "photo",
        "year": 1890,
        "resolution": "1111"
    }
    with pytest.raises(InvalidEntityError):
        MediaItem.from_dict(data)

def test_zero_duration_for_video():
    data = {
        "id": "3",
        "name": "video",
        "category": "video",
        "year": 1890,
        "resolution": "HD",
        "duration": 0
    }
    with pytest.raises(InvalidEntityError):
        MediaItem.from_dict(data)

def test_minus_duration():
    data = {
        "id": "3",
        "name": "Photo 1",
        "category": "photo",
        "year": 1890,
        "resolution": "SD",
        "duration": -1
    }
    with pytest.raises(InvalidEntityError):
        MediaItem.from_dict(data)

def test_positive_duration_for_photo():
    data = {
        "id": "3",
        "name": "Photo 1",
        "category": "photo",
        "year": 1890,
        "resolution": "SD",
        "duration": 10
    }
    with pytest.raises(InvalidEntityError):
        MediaItem.from_dict(data)

def test_no_field():
    data = {
        "id": "3",
        "category": "photo",
        "year": 1890,
        "resolution": "SD",
        "duration": -1
    }
    with pytest.raises(BrokenDataError):
        MediaItem.from_dict(data)

def test_to_dict_from_dict_roundtrip():
    data = {
        "id": "1",
        "name": "Матрица",
        "category": "фильм",
        "year": 1999,
        "resolution": "1920x1080",
        "duration": 9000,
    }
    original = MediaItem.from_dict(data)
    restored = MediaItem.from_dict(original.to_dict())
    assert restored == original