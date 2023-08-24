import asyncio
import signal
from time import sleep, strftime

from codingTracker.data import Data
from codingTracker.datahandler import DataHandler
from codingTracker.language import LanguageTracker
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
        self.language_tracker: LanguageTracker = LanguageTracker()
        self.data: Data = Data()
        self.data_handler: DataHandler = DataHandler(
            host_ip=host, host_port=port
        )
        self.process_tracker: ProcessTracker = ProcessTracker()
        self.running: bool = True
        self.loop: asyncio.AbstractEventLoop = None

    async def run(self):
        self.loop = asyncio.get_running_loop()
        self.loop.add_signal_handler(
            signal.SIGINT, lambda: asyncio.create_task(self.signal_handler())
        )
        self.loop.add_signal_handler(
            signal.SIGTERM, lambda: asyncio.create_task(self.signal_handler())
        )
        await self.main_loop()

    async def main_loop(self) -> None:
        while self.running:
            new_data: Data = self.update_data()
            await self.save_data()
            sleep(self.sleeping_time)

    def update_data(self) -> Data:
        editor_processes: list[
            EditorProcess
        ] = self.process_tracker.get_processes()
        self.language_tracker.update(editor_processes)
        data: Data= self.language_tracker.get_data()
        return data

    async def save_data(self):
        if len(self.data.data.keys()) > 0:
            await self.data_handler.update(self.data)

    async def signal_handler(self):
        self.sleeping_time = 0
        await self.save_data()
        await self.data_handler.terminate()
        self.running = False


def main() -> None:
    app = App()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
