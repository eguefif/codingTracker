import asyncio
import json

import pytest


@pytest.fixture
def data():
    data: dict[str, dict[str, int]] = {"123 2023": {"python": 23, "c": 10}}
    return data


@pytest.mark.asyncio
async def t(data):
    reader, writer = await asyncio.open_connection("127.0.0.1", 10000)
    message = json.dumps(data)
    size = len(message)
    protoheader = "{0:3}".format(size)
    print(protoheader)
    writer.write(protoheader.encode("utf-8"))
    writer.write(message.encode("utf-8"))
    await writer.drain()
    retval: str = "-1"
    retval = await reader.read(1)
    assert retval.decode("utf-8") == "1"
