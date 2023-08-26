import asyncio
import signal
import json

async def run_server() -> None:
    server = await asyncio.start_server(handle_input, "127.0.0.1", 10000)
    async with server:
        await server.serve_forever()

async def handle_input(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    print("New connexion")
    protoheader: bytes  = await reader.read(5)
    size: int = int(protoheader.decode())
    if size > 1:
        message: bytes = await reader.read(size)
        str_message: str = message.decode()
        retval: str = str(size) + str_message
        print(retval)
        with open("./tests/temp", "w") as f:
            f.write(retval)

if __name__ == "__main__":
    asyncio.run(run_server())
