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
        self.connexion: Connexion = Connexion(host=host, port=port, encoding=encoding)
        self.file_handler: FileData = FileData(path=file_path)
        self.encoding = encoding

    async def on_init(self):
        try:
            await self.connexion.init_connection()
        except Exception as e:
            print("Exception while initialize connexion ", e)

    async def update(self, data: Data):
        if self.connexion.state:
            await self.connexion.update(data)
        else:
            self.file_handler.save(data)

    def erase_data(self) -> None:
        self.file_handler.erase_data()

    async def is_synced(self) -> bool:
        retval: bool = await self.connexion.is_data_synced()
        if retval:
            return True
        return False

    async def terminate(self):
        await self.connexion.terminate_connection()
