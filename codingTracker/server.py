import asyncio
import json
import time

from codingTracker.data import FileData

class App:
    def __init__(self, host="127.0.0.1", port=10000):
        self.host: str = host
        self.port: int = port
        self.file: FileData = FileData

    async def process_client(self,
            reader: asyncio.StreamReader,
            writer: asyncio.StreamWriter) -> None:
        print("new connexion with ", writer.get_extra_info("peername"))
        size: str = await self.get_message_size(reader)
        print(size)
        data: dict[str, dict[str, int]] = await self.get_data(reader, 100)
        ret: str = "1"
        writer.write(ret.encode("utf-8"))
        await write.drain()
        self.save_data(data)

    async def get_message_size(self, reader: asyncio.StreamReader) -> int:
        size: bytes = await reader.read(3)
        message = size.decode("utf-8")
        return int(message)

    async def get_data(self, reader: asyncio.StreamReader, size: int):
        message = await reader.read(size)
        message = message.decode("utf-8")
        return json.loads(message)

    def save_data(self, data: dict[str, dict[str, int]]):
        self.file.save(data)

    async def run(self) -> None:
        server = await asyncio.start_server(self.process_client, host=self.host, port=self.port)
        async with server:
            await server.serve_forever()

def main() -> None:
    app: App = App()
    asyncio.run(app.run())

if __name__ == "__main__":
    main()
