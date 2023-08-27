import asyncio
import pytest
import json

from codingTracker.client import App
from codingTracker.data import Data

@pytest.fixture
def app_no_connexion(data_day_object: Data) -> App:
    app = App(file_path="./temp", port=25000)
    app.data = data_day_object
    return app


@pytest.mark.asyncio
async def test_save(app_no_connexion, data_day_object) -> None:
    await app_no_connexion._save_data()
    with open("./data.dat", "r") as f:
        data = f.read()
    assert data == json.dumps(data_day_object.data)


@pytest.fixture
def app_connected(data_day_object) -> None:
    app = App(file_path="./temp", port=10000)
    app.data = data_day_object
    return app


@pytest.mark.asyncio
async def test_save_connected(app_connected, data_day_object, event_loop) -> None:
    await app_connected.data_handler.on_init()
    await app_connected._save_data()
    retval: bytes = await asyncio.wait_for(
            app_connected.data_handler.connexion.reader.read(1), 1)
    assert retval == b"1"

@pytest.mark.asyncio
async def test_save_connected_synced(app_connected, data_day_object, event_loop) -> None:
    await app_connected.data_handler.on_init()
    await app_connected._save_data()
    await app_connected._check_synced()
    with open(app_connected.data_handler.file_handler.path, "r") as f:
        content = f.read()
    assert content == '{}'
    assert app_connected.data.data == {}

