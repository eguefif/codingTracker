import asyncio
import signal

from codingTracker.data import Data
from codingTracker.datahandler import DataHandler
from codingTracker.process import EditorProcess, ProcessTracker


class App:
    def __init__(
        self,
        sleeping_time: int = 5,
        host="127.0.0.1",
        port=10000,
        file_path="./data.dat",
        encoding="utf-8",
    ):
        self.sleeping_time = sleeping_time
        self.running: bool = True
        self.loop: asyncio.AbstractEventLoop = None

        self.data_handler: DataHandler = DataHandler(
            file_path=file_path,
            host=host,
            port=port,
            encoding="utf-8",
        )
        self.data: Data = Data()
        self.process_tracker: ProcessTracker = ProcessTracker()

    async def on_init(self):
        self._configure_signals()
        await self.data_handler.on_init()

    def _configure_signals(self):
        self.loop = asyncio.get_running_loop()
        self.loop.add_signal_handler(
            signal.SIGINT, lambda: asyncio.create_task(self._signal_handler())
        )
        self.loop.add_signal_handler(
            signal.SIGTERM, lambda: asyncio.create_task(self._signal_handler())
        )

    async def run(self) -> None:
        await self.on_init()
        while self.running:
            self._update_data()
            await self._save_data()
            await asyncio.wait_for(self._check_synced(), 1)

    def _update_data(self) -> None:
        editor_list: list[EditorProcess] = self.process_tracker.get_processes()
        self.data.update(editor_list)

    async def _save_data(self):
        await self.data_handler.update(self.data)

    async def _check_synced(self) -> None:
        retval: bool = await self.data_handler.is_synced()
        if retval:
            self.data_handler.erase_data()
            self.data.reset_data()

    async def _signal_handler(self):
        await self._save_data()
        await self.data_handler.terminate()
        self.running = False


def main() -> None:
    app = App()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
