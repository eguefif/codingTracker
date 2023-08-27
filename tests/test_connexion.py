import json

import pytest

from codingTracker.connexion import Connexion, Data


@pytest.fixture
def data() -> tuple[Data, dict[str, dict[str, list[float]]]]:
    data_dict: dict[str, dict[str, list[float]]] = {
        "123 2023": {"python": [32.1, 11.3], "c": [22, 23.1]},
        "100 2022": {"python": [12, 32.2]},
    }
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
    assert connexion.state is False


@pytest.mark.asyncio
async def test_init_connection(connexion) -> None:
    await connexion.init_connection()
    state: bool = connexion.state
    assert state is True


@pytest.mark.asyncio
async def test_terminate_connection(connexion) -> None:
    await connexion.init_connection()
    await connexion.terminate_connection()
    assert connexion.state is False
    assert connexion.writer.is_closing()
