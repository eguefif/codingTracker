from codingTracker.connexion import Connexion
from codingTracker.data import Data, FileData


class DataHandler:
    def __init__(
        self,
        nodata=False,
        file_path="./data.dat",
        host_ip="127.0.0.1",
        host_port=10000,
        encoding="utf-8",
    ) -> None:
        self.file_handler: FileData = FileData(nodata=False, path=file_path)
        self.connexion: Connexion = Connexion(host_ip, host_port)
        self.encoding = encoding

    async def init_connection(self):
        try:
            await self.connexion.init_connection()
        except Exception as e:
            print("Failed connection to server: ", e)
            self.connexion.state = False

    async def update(self, data: Data):
        retval: bool = await self.update_server(data)
        if not retval or self.connexion.state == False:
            self.file_handler.save(data)

    async def update_server(self, new_data: Data) -> bool:
        check: bool = False
        if self.connexion.state:
            try:
                await self.connexion.update(new_data)
                check = await self.connexion.is_data_synced()
            except Exception:
                print("Connection lost. Saving locally.")
                self.connexion.state = False
                return False
            if check:
                self.file_handler.erase_data()
                return True
        else:
            await self.init_connection()
        return False

    def build_data(self, data: Data) -> Data:
        file_data: Data = self.file_handler.get_whole_data(data)
        return file_data

    async def terminate(self):
        await self.connexion.terminate_connection()

    def get_data_from_file(self):
        data: dict[str, dict[str, [float, float]]] = None
        with open(self.file_path, "r") as f:
            content: str = f.read()
        if len(content) > 2:
            data = json.
