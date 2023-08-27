import json
from time import strftime

import pytest

from codingTracker.data import FileData


@pytest.fixture
def temp_data_file(data_day_object) -> None:
    with open("./tests/temp", "w") as f:
        json.dump(data_day_object.data, f)


@pytest.fixture
def empty_file() -> None:
    with open("./tests/temp", "w") as f:
        f.write("")


def test_constructor_from_data_in_file(data_day_object, temp_data_file) -> None:
    file_handler: FileData = FileData(path="./tests/temp")
    assert file_handler.data.data == data_day_object.data


def test_constructor_file_empty(empty_file) -> None:
    day: str = strftime("%j %y")
    file_handler: FileData = FileData(path="./tests/temp")
    assert file_handler.data.data == {day: {}}


def test_save(data_day_object) -> None:
    file_handler: FileData = FileData()
    file_handler.save(data_day_object)
    with open("./data.dat", "r") as f:
        retval = json.load(f)
    assert data_day_object.data == retval


def test_is_data_true(temp_data_file) -> None:
    file_handler: FileData = FileData(path="./tests/temp")
    assert file_handler


def test_is_data_false(empty_file) -> None:
    file_handler: FileData = FileData(path="./tests/temp")
    assert not file_handler.is_data()


def test_erase_data(temp_data_file) -> None:
    file_handler: FileData = FileData(path="./tests/temp")
    file_handler.erase_data()
    assert not file_handler.is_data()


def test_erase_data_empty_file(empty_file) -> None:
    file_handler: FileData = FileData(path="./tests/temp")
    file_handler.erase_data()
    assert not file_handler.is_data()
