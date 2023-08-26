import asyncio
import json
import signal

from codingTracker.data import Data, FileData


class GraceFullExit(SystemExit):
    pass


def shutdown():
    raise GraceFullExit


class App:
    def __init__(self, host="127.0.0.1", port=10000) -> None:
        self.host: str = host
        self.port: int = port
        self.file: FileData = FileData(nodata=False, path="./data_server.dat")
        self.running: bool = True
        self.clients: list[asyncio.StreamWriter] = []
        self.tasks: list[asyncio.Task] = []

    async def process_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        print("new connexion with ", writer.get_extra_info("peername"))
        self.clients.append(writer)
        task: asyncio.Task = asyncio.create_task(self.listen(reader, writer))
        self.tasks.append(task)

    async def listen(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        while True:
            data: dict[str, dict[str, list[float]]] = {}
            size: int = await self.get_message_size(reader)
            if size == -1:
                break
            data = await self.get_data(reader, size)
            if data == "\0":
                break
            print(data)
            if len(data) > 0:
                ret: str = "1"
            else:
                ret = "0"
            writer.write(ret.encode("utf-8"))
            await writer.drain()
            self.save_data(data)

    async def get_message_size(self, reader: asyncio.StreamReader) -> int:
        size: bytes = await reader.read(5)
        message = size.decode("utf-8")
        if message == "\0" or message == "":
            return -1
        return int(message)

    async def get_data(self, reader: asyncio.StreamReader, size: int):
        encoded_message = await reader.read(size)
        message = encoded_message.decode("utf-8")
        return json.loads(message)

    def save_data(self, dict_data: dict[str, dict[str, list[float]]]):
        data: Data = Data(dict_data)
        self.file.save(data)

    async def terminate_server(self) -> None:
        for writer in self.clients:
            if not writer.is_closing():
                try:
                    writer.close()
                except Exception as e:
                    print("Closing streams exception: ", e)
                await writer.wait_closed()

    async def run(self) -> None:
        self.server = await asyncio.start_server(
            self.process_client, host=self.host, port=self.port
        )
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, shutdown)
        loop.add_signal_handler(signal.SIGINT, shutdown)
        try:
            await self.server.serve_forever()
        except GraceFullExit:
            await self.terminate_server()
        finally:
            self.server.close()
            await self.server.wait_closed()


def main() -> None:
    app: App = App()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
