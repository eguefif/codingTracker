import pytest
import json

from codingTracker.data import Data, FileData

self.day_format: str = "%j %y"

@pytest.fixture
def filedata_object() -> FileData:
    test_path: str = "./tests/data.dat"
    datap_obj: FileData = FileData(nodata=True, path=test_path)
    with open(test_path, "w") as f:
        f.write("{}")
    return datap_obj

@pytest.fixture
def filedata_object_filled() -> FileData:
    test_path: str = "./tests/data.dat"
    datap_obj: FileData = FileData(nodata=True, path=test_path)
    with open(test_path, "w") as f:
        json.dump("{'python': 23, 'c': 22}", f)
    return datap_obj

@pytest.fixture
def empty_data_object() -> Data:
    data: Data = Data()
    return data

def test_update_data(empty_data_object, filedata_object):
    data: dict[str, dict[str, int]] = {"python": 15, "javascript": 12, "c": 23}
    empty_data_object.update(data)
    filedata_object.save(empty_data_object.data)
    data_ret = filedata_object.get_data_from_file()

    assert data_ret["python"] == 15
    assert data_ret["javascript"] == 12
    assert data_ret["c"] == 23


def test_update_data_twice(empty_data_object, filedata_object):
    for i in range(1, 2):
        data = {"python": 15 * i, "javascript": 12 * i, "c": 23 * i}
        empty_data_object.update(data)
        filedata_object.save(empty_data_object.data)
        data_ret = filedata_object.get_data_from_file()
        assert data_ret["python"] == 15 * i
        assert data_ret["javascript"] == 12 * i
        assert data_ret["c"] == 23 * i

def test_is_data_false(filedata_object) -> None:
   assert filedata_object.is_data() == False

def test_is_data_true(filedata_object_filled) -> None:
   assert filedata_object_filled.is_data() == True

def test_erase_data(filedata_object_filled) -> None:
    filedata_object_filled.erase_data()
    with open(filedata_object_filled.path, "r") as f:
        content = f.read()
    assert len(content) == 2

def test_get_data_from_file(filedata_object_filled) -> None:
    content = filedata_object_filled.get_data_from_file()
    assert content["python"] == 15
    assert content["c"] == 22
