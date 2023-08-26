import pytest
import json
from time import time, strftime

from codingTracker.data import Data, FileData
from codingTracker.process import EditorProcess

DAY_FORMAT: str = "%j %y"

@pytest.fixture
def empty_data_object() -> Data:
    data: Data = Data()
    return data

@pytest.fixture
def data_day_object() -> Data:
    day: str = strftime(DAY_FORMAT)
    data_dict: dict[str, dict[str, int]] = {
                                            day: {"python": [21.12, 41.23],
                                            "javascript": [21.12, 41.23],
                                            "c++": [21.12, 41.23],
                                            "c": [21.12, 41.2]},
                                            "110 2023": {"python": [21.12, 41.23],
                                            "javascript": [21.12, 41.23],
                                            "c": [21.12, 41.2]},
                                            "111 2023": {"python": [21.12, 41.23],
                                            "javascript": [21.12, 41.23],
                                            "c": [21.12, 41.2]}}
    data: Data = Data(data_dict)
    return data

@pytest.fixture
def processes() -> list[str]:
    ps_entries = [
        "eguefif     33464  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py",
        "guefif     33  0.2  0.0  33 33516 pts/0    S+   06:46   0:00 vim test.c",
        "guefif     22222  0.2  0.0  22222 11648 pts/0    S+   06:46   0:00 emacs test.js",
    ]
    retval = [EditorProcess(entry) for entry in ps_entries]
    return retval

def test_update_data_with_empty_data_object(empty_data_object, processes):
    day: str = strftime(DAY_FORMAT)
    start_time: float = time()
    empty_data_object.update(processes)
    assert start_time - 1 < empty_data_object.data[day]["python"][0] < start_time + 1 
    assert start_time - 1 < empty_data_object.data[day]["python"][1] < start_time + 1 
    assert start_time - 1 < empty_data_object.data[day]["c"][0] < start_time + 1 
    assert start_time - 1 < empty_data_object.data[day]["c"][1] < start_time + 1 
    assert start_time - 1 < empty_data_object.data[day]["javascript"][0] < start_time + 1 
    assert start_time - 1 < empty_data_object.data[day]["javascript"][1] < start_time + 1 


def test_update_data_with_data_of_the_day_already(data_day_object, processes):
    day: str = strftime(DAY_FORMAT)
    start_time: float = 21.12 
    data_day_object.update(processes)
    end_time: float = time()
    assert data_day_object.data[day]["python"][0] == start_time
    assert end_time -1  < data_day_object.data[day]["python"][1] < end_time + 1
    assert data_day_object.data[day]["c"][0] < start_time + 1
    assert end_time - 1 < data_day_object.data[day]["c"][1] < end_time + 1
    assert data_day_object.data[day]["javascript"][0] == start_time
    assert end_time - 1 < data_day_object.data[day]["javascript"][1] < end_time + 1
    assert data_day_object.data[day]["c++"][0] == start_time
    assert data_day_object.data[day]["c++"][1] == 41.23
