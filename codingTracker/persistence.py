from codingTracker.connexion import Connexion
from codingTracker.session import Session, SessionTracker
from codingTracker.sqlhandler import SqlHandler
from codingTracker.process import EditorProcess


class Persistence:
    def __init__( self,
            file_path: str = None,
            host: str = None,
            port: int = None,
            encoding: str = None,
    ) -> None:
        self.connexion: Connexion = Connexion(host=host, port=port, encoding=encoding)
        self.sql: SqlHandler = SqlHandler(file_path)
        self.encoding = encoding
        data: list[tuple[str, float, float, bool]] = self.sql.get_data()
        self.sessions = SessionTracker(data)

    async def on_init(self):
        try:
            await self.connexion.init_connection()
        except Exception as e:
            print("Exception while initialize connexion ", e)

    async def update(self, editors: list[EditorProcess]):
        self.sessions.update(editors)
        if self.connexion.state:
            await self.connexion.update(self.sessions)
        else:
        self.sql.update(self.sessions.data)

    def erase_data(self) -> None:
        self.file_handler.erase_data()

    async def is_synced(self) -> bool:
        retval: bool = await self.connexion.is_data_synced()
        if retval:
            return True
        return False

    async def terminate(self):
        await self.connexion.terminate_connection()
        self.sql.terminate()
