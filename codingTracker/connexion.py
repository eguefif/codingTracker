import asyncio
import json

from codingTracker.data import Data


class Connexion:
    def __init__(self, host="127.0.0.1", port=10000, encoding="utf-8") -> None:
        self.host = host
        self.port = port
        self.data: bytes = b""
        self.encoding = encoding
        self.state: bool = False

    async def init_connection(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(
                self.host, self.port
            )
        except Exception as e:
            print(f"Exception while connecting: {e}")
            self.state = False
            return
        self.state = True

    async def update(self, data: Data) -> None:
        message = self.get_encoded_message(data)
        await self.send_protoheader(message)
        await self.send(message)

    def get_encoded_message(self, data: Data) -> bytes:
        dump: str = json.dumps(data.data)
        encoded_message: bytes = dump.encode(self.encoding)
        return encoded_message

    async def send_protoheader(self, message: bytes) -> None:
        protoheader: bytes = self.build_protoheader(message)
        await self.send(protoheader)

    def build_protoheader(self, message: bytes) -> bytes:
        protoheader: str = "{0:5}".format(len(message))
        return protoheader.encode(self.encoding)

    async def send(self, message: bytes) -> None:
        print("sending : ", message)
        self.writer.write(message)
        await self.writer.drain()

    async def is_data_synced(self) -> bool:
        retval: bytes = await self.reader.read(1)
        message: str = retval.decode(self.encoding)
        if message == "1":
            return True
        return False

    async def terminate_connection(self) -> None:
        if self.state:
            self.writer.write_eof()
            self.writer.close()
            await self.writer.wait_closed()
            self.state = False
