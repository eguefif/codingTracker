import asyncio
import signal
from time import sleep

from codingTracker.data import Data
from codingTracker.datahandler import DataHandler
from codingTracker.process import EditorProcess, ProcessTracker


class App:
    def __init__(
        self,
        sleeping_time: int = 5,
        host="127.0.0.1",
        port=10000,
        data="./data.dat",
        encoding="utf-8",
    ):
        self.sleeping_time = sleeping_time
        self.running: bool = True
        self.loop: asyncio.AbstractEventLoop = None

        self.data_handler: DataHandler = DataHandler(
            file_path="./data.dat",
            host=host,
            port=port,
            encoding="utf-8",
        )
        self.data: Data = Data()
        self.process_tracker: ProcessTracker = ProcessTracker()

    def on_init(self):
        self.configure_signal()
        self.data_handler.init_connection()

    async def run(self) -> None:
        while self.running:
            editor_list: list[
                EditorProcess
            ] = self.process_tracker.get_processes()
            new_data: Data = Data()
            new_data.update(editor_list)
            await self.save_data(new_data)
            sleep(self.sleeping_time)

    def configure_signals(self):
        self.loop = asyncio.get_running_loop()
        self.loop.add_signal_handler(
            signal.SIGINT, lambda: asyncio.create_task(self.signal_handler())
        )
        self.loop.add_signal_handler(
            signal.SIGTERM, lambda: asyncio.create_task(self.signal_handler())
        )

    async def save_data(self, new_data: Data):
        if len(self.data.data.keys()) > 0:
            await self.data_handler.update(new_data)

    async def signal_handler(self):
        await self.save_data()
        await self.data_handler.terminate()
        self.running = False


def main() -> None:
    app = App()
    app.on_init()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
