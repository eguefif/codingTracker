from codingTracker.connexion import Connexion
from codingTracker.data import Data, FileData


class DataHandler:
    def __init__(
        self,
        file_path="./data.dat",
        host="127.0.0.1",
        port=10000,
        encoding="utf-8",
    ) -> None:
        self.file_handler: FileData = FileData(path=file_path)
        self.connexion: Connexion = Connexion(host=host, port=port)
        self.encoding = encoding

    async def on_init(self):
        await self.connexion.init_connection()

    async def update(self, data: Data):
        check: bool = False
        if self.connexion.state is True:
            await self.connexion.update(data)
            check = await self.connexion.is_data_synced()
        if not check or self.connexion.state is False:
            self.file_handler.save(data)

    async def terminate(self):
        await self.connexion.terminate_connection()
