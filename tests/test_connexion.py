import pytest
import json
import asyncio
from xprocess import ProcessStarter


from codingTracker.connexion import Connexion
from codingTracker.connexion import Data


@pytest.fixture
def connexion() -> Connexion:
    return Connexion()

@pytest.fixture
def data() -> Data:
    data_dict: dict[str, dict[str, list[float]]] = {"123 2023": {"python": [32.1, 11.3], "c": [22, 23.1]}, "100 2022": {"python": [12, 32.2]}}
    data_obj: Data = Data(data_dict)
    return data_obj, data_dict


def test_get_encoded_message(connexion, data) -> None:
    data_obj, data_test = data
    dump_test: str = json.dumps(data_test)
    encoded_test: bytes = dump_test.encode()
    encoded_data: bytes = connexion.get_encoded_message(data_obj)
    assert encoded_data == encoded_test

def test_constructor_with_no_connection() -> None:
    connexion = Connexion(host="123.0.0.1", port="12000")
    assert connexion.state == False

@pytest.mark.asyncio
async def test_init_connection(connexion) -> None:
    await connexion.init_connection()
    state: bool = connexion.state
    assert state == True

def get_server_retval() -> str:
    with open("./tests/temp", "r") as f:
        content = f.read()
    return content.strip()

@pytest.mark.asyncio
async def test_update(connexion, data) -> None:
    data_obj, data_test = data
    str_data: str = json.dumps(data_test)
    protoheader: str = f"{len(str_data)}"
    message: str = protoheader + str_data
    await connexion.init_connection()
    await connexion.update(data_obj)
    retval: str = get_server_retval()
    assert retval == message

@pytest.mark.asyncio
async def test_terminate_connection(connexion) -> None:
    await connexion.init_connection()
    await connexion.terminate_connection()
    assert connexion.state == False
    assert connexion.writer.is_closing()
