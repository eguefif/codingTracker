import asyncio

from codingTracker.data import Data


class Connexion:
    def __init__(self, host="127.0.0.1", port=10000, encoding="utf-8") -> None:
        self.host = host
        self.port = port
        self.data: bytes = b""
        self.encoding = encoding
        self.state: bool = False

    async def init_connection(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.host, self.port
        )
        if self.writer.get_extra_info("peername") is None:
            self.state = False
        else:
            self.state = True

    async def update(self, data: Data) -> None:
        self.data = self.transform_data_for_remote(data)
        await self.send_protoheader()
        await self.send_data()

    def transform_data_for_remote(self, data: Data) -> bytes:
        return data.get_data_for_sending()

    async def send_protoheader(self) -> None:
        protoheader: bytes = self.build_protoheader()
        await self.send(protoheader)

    def build_protoheader(self) -> bytes:
        protoheader: str = "{0:5}".format(len(self.data))
        return protoheader.encode(self.encoding)

    async def send_data(self) -> None:
        await self.send(self.data)

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
            self.writer.wait_closed()
