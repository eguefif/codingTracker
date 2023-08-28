import asyncio
import json
from time import strftime

import pytest

from codingTracker.server import App

today: str = strftime("%j %y")


@pytest.fixture
def data_dict() -> dict[str, dict[str, list[float]]]:
    data = {
        "112 2023": {
            "python": [12.0, 13.0],
            "javascript": [12.0, 15.0],
            "c": [13.0, 16.0],
        },
        "111 2023": {
            "python": [11.0, 13.0],
            "javascript": [12.0, 16.0],
            "c": [19.0, 20.0],
        },
        "110 2022": {
            "python": [10.0, 15.0],
            "javascript": [15.0, 19.0],
            "c": [18.0, 24.0],
        },
    }

    return data


@pytest.fixture
def server_app() -> App:
    with open("./tests/temp", "w") as f:
        f.write("{}")
    app = App(path="./tests/temp")
    return app


def test_save_data_with_empty_file(data_dict, server_app) -> None:
    server_app.save_data(data_dict)
    with open("./tests/temp", "r") as f:
        content: dict[str, dict[str, list[float]]] = json.load(f)
    assert content == data_dict


def write_in_file() -> None:
    data = {
        "112 2023": {"python": [12, 13], "javascript": [12, 15], "c": [13, 16]},
        "111 2023": {"python": [11, 13], "javascript": [12, 16], "c": [19, 20]},
        "110 2022": {"python": [10, 15], "javascript": [15, 19], "c": [18, 24]},
    }
    with open("./tests/temp", "w") as f:
        json.dump(data, f)


data_to_test = [
    (
        {
            "112 2023": {
                "python": [12, 15],
                "javascript": [12, 16],
                "c": [13, 18],
            }
        },
        {
            today: {},
            "112 2023": {
                "python": [12, 15],
                "javascript": [12, 16],
                "c": [13, 18],
            },
            "111 2023": {
                "python": [11, 13],
                "javascript": [12, 16],
                "c": [19, 20],
            },
            "110 2022": {
                "python": [10, 15],
                "javascript": [15, 19],
                "c": [18, 24],
            },
        },
    ),
    (
        {
            "109 2023": {
                "python": [11, 13],
                "javascript": [12, 16],
                "c": [19, 20],
            }
        },
        {
            today: {},
            "112 2023": {
                "python": [12, 13],
                "javascript": [12, 15],
                "c": [13, 16],
            },
            "111 2023": {
                "python": [11, 13],
                "javascript": [12, 16],
                "c": [19, 20],
            },
            "110 2022": {
                "python": [10, 15],
                "javascript": [15, 19],
                "c": [18, 24],
            },
            "109 2023": {
                "python": [11, 13],
                "javascript": [12, 16],
                "c": [19, 20],
            },
        },
    ),
]


@pytest.mark.parametrize("test_input, test_output", data_to_test)
def test_save_data_with_data_in_file(
    server_app, test_input, test_output
) -> None:
    write_in_file()
    server_app.save_data(test_input)
    with open("./tests/temp", "r") as f:
        content: dict[str, dict[str, list[float]]] = json.load(f)
    assert test_output == content


@pytest.mark.asyncio
async def test_server(data_dict) -> None:
    reader, writer = await asyncio.open_connection("127.0.0.1", 10000)
    content_dump: str = json.dumps(data_dict)
    protoheader_str: str = "{0:5}".format(len(content_dump))
    protoheader: bytes = protoheader_str.encode()
    content: bytes = content_dump.encode()
    writer.write(protoheader)
    await writer.drain()
    writer.write(content)
    await writer.drain()
    retval: bytes = await reader.read(1)
    assert retval == b"1"


@pytest.mark.asyncio
async def test_server_no_data() -> None:
    reader, writer = await asyncio.open_connection("127.0.0.1", 10000)
    content_dump: str = ""
    protoheader_str: str = "{0:5}".format(len(content_dump))
    protoheader: bytes = protoheader_str.encode()
    content: bytes = content_dump.encode()
    writer.write(protoheader)
    await writer.drain()
    writer.write(content)
    await writer.drain()
    retval: bytes = await reader.read(1)
    assert retval == b"0"
