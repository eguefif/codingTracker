#!/bin/python3
import asyncio
import signal
import json
import sys

class serverForTest:
    def __init__(self) -> None:
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    async def run_server(self) -> None:
        self.server = await asyncio.start_server(self.handle_input, "127.0.0.1", 10000)
        async with self.server:
            await self.server.serve_forever()

    async def handle_input(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        protoheader: bytes  = await reader.read(5)
        if len(protoheader) == 5:
            size: int = int(protoheader.decode())
            message: bytes = await reader.read(size)
            str_message: str = message.decode()
            retval: str = str(size) + str_message
            with open("./tests/temp", "w") as f:
                f.write(retval)
            writer.write(b"1")
            await writer.drain()

    def signal_handler(self, sig, frame):
        self.server.close()
        sys.exit()


if __name__ == "__main__":
    server = serverForTest()
    asyncio.run(server.run_server())
