import asyncio
import json
import signal
import sys
from pathlib import Path
from time import sleep

from codingTracker.persistence import Persistence
from codingTracker.process import EditorProcess, EditorTracker


class App:
    def __init__(
        self,
        sleeping_time: int = 5,
        host: str ="127.0.0.1",
        port: int =10000,
        path: str ="./data.dat",
        encoding: str="utf-8",
        cfg_file_path: str = "./client.cfg",
    ):
        cfg_path: Path = Path(cfg_file_path)
        if cfg_path.exists():
            with open(cfg_path, "r") as f:
                cfg_file: dict[str, int | str] = json.load(f)
            self.sleeping_time: int = cfg_file["sleeping_time"]
            self.persistence: Persistence = Persistence(
                file_path=cfg_file["path"],
                host=cfg_file["ip"],
                port=cfg_file["port"],
                encoding=cfg_file["encoding"],
            )
        else:
            self.sleeping_time = sleeping_time
            self.loop: asyncio.AbstractEventLoop = None
            self.persistence = Persistence(
                file_path=path,
                host=host,
                port=port,
                encoding="utf-8",
            )
        self.running: bool = True
        self.editor_tracker: EditorTracker = EditorTracker()

    async def run(self) -> None:
        await self.on_init()
        while self.running:
            await self._update_data()
            #await asyncio.wait_for(self._check_synced(), 1)
            await asyncio.sleep(self.sleeping_time)

    async def on_init(self):
        self._configure_signals()
        await self.persistence.on_init()

    def _configure_signals(self):
        self.loop = asyncio.get_running_loop()
        self.loop.add_signal_handler(
            signal.SIGINT, lambda: asyncio.create_task(self._signal_handler())
        )
        self.loop.add_signal_handler(
            signal.SIGTERM, lambda: asyncio.create_task(self._signal_handler())
        )

    async def _update_data(self) -> None:
        editors: list[EditorProcess] = self.editor_tracker.get_editors()
        await self.persistence.update(editors)

    async def _check_synced(self) -> None:
        retval: bool = await self.persistence.is_synced()
        if retval:
            self.persistence.erase_data()
            self.data.reset_data()

    async def _signal_handler(self):
        await self._update_data()
        await self.persistence.terminate()
        self.running = False


def main() -> None:
    if len(sys.argv) > 1:
        if len(sys.argv) == 4:
            app = App(host=sys.argv[1], port=int(sys.argv[2]), path=sys.argv[3])
        else:
            print("Usage: codingTracker HOST_IP PORT DATA_PATH")
            sys.exit()
    else:
        app = App()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
