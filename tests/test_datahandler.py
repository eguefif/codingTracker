import json

import pytest

from codingTracker.data import Data
from codingTracker.datahandler import DataHandler


@pytest.fixture
def data_handler_disconnected() -> DataHandler:
    data_handler: DataHandler = DataHandler(host="129.0.0.1", port=11000)
    return data_handler


@pytest.mark.asyncio
async def test_update_no_connexion(
    data_handler_disconnected: DataHandler, data_day_object: Data
) -> None:
    # await data_handler_disconnected.on_init()
    await data_handler_disconnected.update(data_day_object)
    with open("./data.dat", "r") as f:
        data = json.load(f)
    print(data_day_object.data)
    print(data)
    assert data_day_object.data == data


@pytest.fixture
def data_handler_connected() -> DataHandler:
    data_handler: DataHandler = DataHandler()
    return data_handler


@pytest.mark.asyncio
async def test_update_connexion(
    data_handler_connected: DataHandler, data_day_object: Data
) -> None:
    await data_handler_connected.on_init()
    await data_handler_connected.update(data_day_object)
    with open("./tests/temp", "r") as f:
        data: str = f.read()
    dump = json.dumps(data_day_object.data)
    test_message = f"{len(dump)}" + dump
    await data_handler_connected.terminate()
    assert test_message == data
