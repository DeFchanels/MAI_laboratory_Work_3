import pytest
from pygments.lexers import data

from src.media_catalog.media_catalog import MediaCatalog
from src.media_catalog.media_item import MediaItem
from src.media_catalog.errors import InvalidEntityError, IdError, NotFoundError


def test_add_increases_len():
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=9000,
    )
    item = MediaItem.from_dict(data)
    cat = MediaCatalog()
    assert len(cat) == 0
    cat.add(item)
    assert len(cat) == 1


def test_add_duplicate_id_raises_id_error():
    cat = MediaCatalog()
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=9000,
    )
    data2 = dict(
        id="1",
        name="Photo",
        category="фото",
        year=1999,
        resolution="1920x1080",
        duration=0,
    )
    assert len(cat) == 0
    cat.add(MediaItem.from_dict(data))
    assert len(cat) == 1
    with pytest.raises(IdError):
        cat.add(MediaItem.from_dict(data2))
    assert len(cat) == 1

def test_add_non_media_item_raises_invalid():
    cat = MediaCatalog()
    with pytest.raises(InvalidEntityError):
        cat.add("not a media")

def test_get_returns_same_object():
    data = dict(
        id="23",
        name="Photo",
        category="фото",
        year=1999,
        resolution="1920x1080",
        duration=0,
    )
    cat = MediaCatalog()
    item = MediaItem.from_dict(data)
    cat.add(item)
    assert cat.get("23") is item

def test_get_missing_raises_not_found():
    cat = MediaCatalog()
    with pytest.raises(NotFoundError):
        cat.get("1")

def test_remove_existing():
    data = dict(
        id="23",
        name="Photo",
        category="фото",
        year=1999,
        resolution="1920x1080",
        duration=0,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    assert len(cat) == 1
    cat.remove("23")
    assert len(cat) == 0
    assert "23" not in cat

def test_remove_missing_raises_not_found():
    cat = MediaCatalog()
    with pytest.raises(NotFoundError):
        cat.remove("1")

def test_remove_last_in_category_clears_index():
    data = dict(
        id="1",
        name="Photo",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    assert cat.find_by_category("фильм") == [MediaItem.from_dict(data)]
    cat.remove("1")
    assert cat.find_by_category("фильм") == []


def test_contains():
    data = dict(
        id="1",
        name="Photo",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    assert "1" in cat
    assert "2" not in cat


def test_find_by_category():
    data = dict(
        id="1",
        name="Photo",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    data2 = dict(
        id="2",
        name="Photo",
        category="фото",
        year=1999,
        resolution="1920x1080",
        duration=0,
    )
    data3 = dict(
        id="3",
        name="Photo",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    cat.add(MediaItem.from_dict(data2))
    cat.add(MediaItem.from_dict(data3))
    assert [i.id for i in cat.find_by_category("фильм")] == ["1", "3"]

def test_find_by_category_empty_returns_empty_list():
    cat = MediaCatalog()
    assert cat.find_by_category("nonexistent") == []

def test_find_by_name():
    data1 = dict(
        id="1",
        name="Photo",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    data2 = dict(
        id="2",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data1))
    cat.add(MediaItem.from_dict(data2))
    assert [i.id for i in cat.find_by_name("МАТРИЦА")] == ["2"]
    assert [i.id for i in cat.find_by_name("матрица")] == ["2"]
    assert [i.id for i in cat.find_by_name("Матрица")] == ["2"]

def test_find_by_name2():
    data1 = dict(
        id="1",
        name="Photo",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    data2 = dict(
        id="2",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data1))
    cat.add(MediaItem.from_dict(data2))
    assert [i.id for i in cat.find_by_name("Рандомное название")] == []

def test_find_by_category_returns_new_list():
    data = dict(
        id="2",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    result = cat.find_by_category("фильм")
    result.append("garbage")
    assert len(cat.find_by_category("фильм")) == 1

def test_iteration_twice_same_order():
    cat = MediaCatalog()
    for i in [1, 3, 2]:
        data = dict(
            id=str(i),
            name="Матрица",
            category="фильм",
            year=1999,
            resolution="1920x1080",
            duration=1000,
        )
        cat.add(MediaItem.from_dict(data))
    assert [i.id for i in cat] == [i.id for i in cat]
    assert [i.id for i in cat] == ['1', '3', '2']

def test_replace_catalog():
    cat = MediaCatalog()
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    data2 = dict(
        id="2",
        name="Матрица 3",
        category="photo",
        year=1999,
        resolution="1920x1080",
    )
    data3 = dict(
        id="3",
        name="Матрица 2",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    cat.add(MediaItem.from_dict(data))

    other = MediaCatalog()
    other.add(MediaItem.from_dict(data2))
    other.add(MediaItem.from_dict(data3))

    cat.replace_catalog(other)
    assert [i.id for i in cat] == ["2", "3"]
    assert "1" not in cat

def test_replace_catalog_2():
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    data2 = dict(
        id="2",
        name="Матрица",
        category="photo",
        year=1999,
        resolution="1920x1080",
    )
    cat = MediaCatalog()
    other = MediaCatalog()
    other.add(MediaItem.from_dict(data))
    cat.replace_catalog(other)

    other.add(MediaItem.from_dict(data2))
    assert "2" not in cat

def test_merge_with_adds_new():
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    data2 = dict(
        id="2",
        name="Матрица",
        category="photo",
        year=1999,
        resolution="1920x1080",
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    other = MediaCatalog()
    other.add(MediaItem.from_dict(data2))
    cat.merge_with(other)
    assert "1" in cat and "2" in cat

def test_merge_with_replaces_existing():
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    data2 = dict(
        id="1",
        name="Матрица 2",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=1000,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    other = MediaCatalog()
    other.add(MediaItem.from_dict(data2))
    cat.merge_with(other)
    assert cat.get("1").name == "Матрица 2"
    assert len(cat) == 1