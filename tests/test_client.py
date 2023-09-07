import asyncio
import json

import pytest

from codingTracker.client import App
from codingTracker.data import Data


@pytest.fixture
def app_no_connexion(data_day_object: Data) -> App:
    app = App(path="./temp", port=25000)
    app.data = data_day_object
    return app


@pytest.mark.asyncio
async def test_save(app_no_connexion, data_day_object) -> None:
    await app_no_connexion._save_data()
    with open("./data.dat", "r") as f:
        data = f.read()
    assert data == json.dumps(data_day_object.data)


@pytest.fixture
def app_connected(data_day_object) -> App:
    app = App(path="./temp")
    app.data = data_day_object
    return app


@pytest.mark.asyncio
async def test_save_connected(
    app_connected, data_day_object, event_loop
) -> None:
    await app_connected.data_handler.on_init()
    await app_connected._save_data()
    retval: bytes = await asyncio.wait_for(
        app_connected.data_handler.connexion.reader.read(1), 1
    )
    assert retval == b"1"


@pytest.mark.asyncio
async def test_save_connected_synced(
    app_connected, data_day_object, event_loop
) -> None:
    await app_connected.data_handler.on_init()
    await app_connected._save_data()
    await app_connected._check_synced()
    with open(app_connected.data_handler.file_handler.path, "r") as f:
        content = f.read()
    assert content == "{}"
    assert app_connected.data.data == {}


@pytest.fixture
def create_setup_file() -> None:
    test_dict: dict[str, str | int] = {
        "sleeping_time": 15,
        "ip": "127.0.0.2",
        "port": 20000,
        "path": "./data.dat",
        "encoding": "utf-16",
    }
    with open("./client.cfg", "w") as f:
        json.dump(test_dict, f)


def test_setup_file(create_setup_file) -> None:
    app = App()
    assert app.sleeping_time == 15
    assert app.data_handler.connexion.host == "127.0.0.2"
    assert app.data_handler.connexion.port == 20000
    assert app.data_handler.file_handler.path == "./data.dat"
    assert app.data_handler.encoding == "utf-16"
