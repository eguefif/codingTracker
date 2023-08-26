from codingTracker.connexion import Connexion
from codingTracker.data import Data, FileData


class DataHandler:
    def __init__(
        self,
        file_path="./data.dat",
        host_ip="127.0.0.1",
        host_port=10000,
        encoding="utf-8",
    ) -> None:
        self.file_handler: FileData = FileData(nodata=False, path=file_path)
        self.connexion: Connexion = Connexion(host_ip, host_port)
        self.connexion.init_connection()
        self.encoding = encoding

    async def update(self, data: Data):
        await self.connexion.update(data)
        check: bool = await self.connexion.is_data_synced()
        if not check or self.connexion.state is False:
            self.file_handler.save(data)

    def build_data(self) -> Data:
        file_data: Data = self.file_handler.get_data_from_file()
        return file_data

    async def terminate(self):
        await self.connexion.terminate_connection()
