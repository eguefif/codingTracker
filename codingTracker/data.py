import json
from time import localtime, sleep, strftime, time

class Data:
    def __init__(self):
        self.data = {}

    def update(self, new_data):
        for key, value in new_data.items():
            self.data[key] = value


class FileData:
    def __init__(self, nodata=True, path: str = "./data.dat"):
        self.path = path
        self.day_format = "%j %y"
        if not nodata:
            self.data: dict[str, int] = self.get_data_from_file()
        else:
            self.data = {}

    def get_data_from_file(self) -> dict[str, int]:
        content: dict[str, dict[str, int]] = {}
        day: str = ""

        with open(self.path, "r") as f:
            content = json.load(f)
        day = strftime(self.day_format, localtime())
        for key, value in content.items():
            if key == day:
                return value
        return {}

    def save(self, data: dict[str, dict[str, int]]) -> None:
        day = strftime(self.day_format, localtime())
        with open(self.path, "r") as f:
            content = json.load(f)
        if day in content.keys():
            for key, value in data.items():
                content[day][key] = data[key]
        else:
            content[day] = data
        with open(self.path, "w") as f:
            json.dump(content, f)
