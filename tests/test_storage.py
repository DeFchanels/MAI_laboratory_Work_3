import json
import pytest
from src.media_catalog.media_item import MediaItem
from src.media_catalog.media_catalog import MediaCatalog
from src.media_catalog.errors import UnsupportedFormatVersionError, BrokenDataError
from src.media_catalog.storage import save, get_load, load, load_with_edit, FORMAT_VERSION


def test_save_and_load(tmp_path):
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=9000,
    )
    data2 = dict(
        id="2",
        name="Дюна",
        category="фильм",
        year=2000,
        resolution="1920x1080",
        duration=10000,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    cat.add(MediaItem.from_dict(data2))
    path = tmp_path / "catalog.json"
    save(cat, path)
    cat2 = get_load(path)
    assert len(cat2) == 2
    item = cat2.get("1")
    assert (item.id, item.name, item.category, item.year,
            item.resolution, item.duration) == (
        "1", "Матрица", "фильм", 1999, "1920x1080", 9000
    )


def test_format_version(tmp_path):
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=9000,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    path = tmp_path / "catalog.json"
    save(cat, path)
    doc = json.loads(path.read_text())
    assert doc["format_version"] == FORMAT_VERSION
    assert len(doc["items"]) == 1


def test_broken_json(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text("{format_version: 1.0")
    with pytest.raises(BrokenDataError):
        get_load(path)

def test_no_file(tmp_path):
    path = tmp_path / "nonexistent.json"
    with pytest.raises(BrokenDataError):
        get_load(path)


def test_insufficient_fields(tmp_path):
    doc = {
        "format_version": FORMAT_VERSION,
        "items": [{"id": "1"}]
    }
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps(doc))
    with pytest.raises(BrokenDataError):
        get_load(path)


def test_missing_version(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps({"items": []}), encoding="utf-8")
    with pytest.raises(UnsupportedFormatVersionError):
        get_load(path)


def test_unknown_version(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps({"format_version": 999, "items": []})
    )
    with pytest.raises(UnsupportedFormatVersionError):
        get_load(path)


def test_load_broken_json_not_changing_catalog(tmp_path):
    cat = MediaCatalog()
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=9000,
    )
    cat.add(MediaItem.from_dict(data))
    before = [i.id for i in cat]
    path = tmp_path / "catalog.json"
    path.write_text("{broken", encoding="utf-8")
    with pytest.raises(BrokenDataError):
        load(cat, path)
    assert [i.id for i in cat] == before
    assert cat.get("1").name == "Матрица"


def test_load_part_broken_json_not_changing_catalog(tmp_path):
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
        id="2",
        name="Матрица 2",
        category="фильм",
        year=2000,
        resolution="1920x1080",
        duration=9001,
    )
    doc = {
        "format_version": FORMAT_VERSION,
        "items": [
            MediaItem.from_dict(data2).to_dict(),
            {"id": "3"}
        ],
    }
    cat.add(MediaItem.from_dict(data))
    before = [i.id for i in cat]
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(BrokenDataError):
        load(cat, path)
    assert [i.id for i in cat] == before
    assert '2'not in cat
    assert cat.get("1").name == "Матрица"


def test_load(tmp_path):
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=9000,
    )
    data2 = dict(
        id="2",
        name="Матрица 2",
        category="фильм",
        year=2000,
        resolution="1920x1080",
        duration=9001,
    )
    old = MediaCatalog()
    old.add(MediaItem.from_dict(data))
    new = MediaCatalog()
    new.add(MediaItem.from_dict(data2))
    path = tmp_path / "new.json"
    save(new, path)
    load(old, path)
    assert "1" not in old
    assert "2" in old


def test_load_with_edit(tmp_path):
    data = dict(
        id="1",
        name="Матрица",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=9000,
    )
    data2 = dict(
        id="2",
        name="Матрица 2",
        category="фильм",
        year=2000,
        resolution="1920x1080",
        duration=9001,
    )
    data3 = dict(
        id="2",
        name="Матрица 3",
        category="фильм",
        year=1999,
        resolution="1920x1080",
        duration=9000,
    )
    data4 = dict(
        id="3",
        name="Матрица 4",
        category="фильм",
        year=2000,
        resolution="1920x1080",
        duration=9001,
    )
    cat = MediaCatalog()
    cat.add(MediaItem.from_dict(data))
    cat.add(MediaItem.from_dict(data2))
    other = MediaCatalog()
    other.add(MediaItem.from_dict(data3))
    other.add(MediaItem.from_dict(data4))
    path = tmp_path / "catalog.json"
    save(other, path)
    load_with_edit(cat, path)
    assert len(cat) == 3
    assert cat.get("2").name == "Матрица 3"
    assert "3" in cat