import pytest

from codingTracker.data import Data, FileData


@pytest.fixture
def filedata_object() -> FileData:
    datap_obj: FileData = FileData(nodata=True, path="./tests/data.dat")
    return datap_obj


@pytest.fixture
def empty_data_object() -> Data:
    data: Data = Data()
    return data


def test_update_data(empty_data_object, filedata_object):
    data = {"python": 15, "javascript": 12, "c": 23}
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
