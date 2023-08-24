import json


class Data:
    def __init__(self, data: dict[str, dict[str, int]] = None, encoding="utf-8"):
        if data is None:
            self.data: dict[str, dict[str, int]] = {}
        else:
            self.data = data
        self.encoding = encoding

    def get_data_for_sending(self) -> bytes:
        dump: str = json.dumps(self.data)
        encoded: bytes = dump.encode(self.encoding)
        return encoded

    def update_from_remote(self, remote_data: bytes) -> None:
        decoded = remote_data.decode(self.encoding)
        self.data = json.loads(decoded)

    def reset_data(self) -> None:
        self.data = {}


class FileData:
    def __init__(self, nodata=False, path: str = "./data.dat"):
        self.path: str = path
        self.day_format: str = "%j %y"
        self.data: Data = None
        if not nodata:
            self.data = self.get_data_from_file()
        else:
            self.data = Data()

    def get_data_from_file(self) -> Data:
        content: dict[str, dict[str, int]] = {}
        day: str = ""
        with open(self.path, "r") as f:
            content = json.load(f)
        if len(content) > 2:
            data: Data = Data(content)
            return Data
        return Data()

    def save(self, data: dict[str, dict[str, int]]) -> None:
        with open(self.path, "w") as f:
            content = json.dump(data, f)

    def is_data(self) -> bool:
        with open(self.path, "r") as f:
            content = f.read()
        if len(content) > 2:
            return True
        return False

    def erase_data(self) -> None:
        with open(self.path, "w") as f:
            f.write("{}")
