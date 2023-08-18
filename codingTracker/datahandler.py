from codingTracker.data import FileData, Data
from codingTracker.connexion import Connexion


class DataHandler:
    def __init__(self, nodata=True, file_path="./data.dat", host_ip="127.0.0.1", host_port=10000):
        self.file_handler: FileData = FileData(nodata=False, path=file_path)
        self.connexion: Connexion = Connexion(host_ip, host_port)

    def update(self):
        pass

