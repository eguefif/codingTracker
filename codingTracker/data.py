import json
import os
from time import strftime, time

from codingTracker.process import EditorProcess


class Data:
    def __init__(self, data: dict[str, dict[str, list[float]]] = None):
        self.day_format: str = "%j %y"
        self.day = strftime(self.day_format)
        if data is None:
            self.data: dict[str, dict[str, list[float]]] = {}
            self.data[self.day] = {}
        else:
            self.data = data
            if self.day not in self.data.keys():
                self.data[self.day] = {}

    def update(self, editor_list: list[EditorProcess]) -> None:
        for editor in editor_list:
            if self.is_new_language(editor):
                self.update_language(editor)
            else:
                self.add_language(editor)

    def update_from_data(self, new_data: "Data") -> None:
        for date in new_data.data.keys():
            if date in self.data.keys():
                for language in new_data.data[date].keys():
                    if language in self.data[date].keys():
                        self.data[date][language][1] = new_data.data[date][
                            language
                        ][1]
                    else:
                        self.data[date][language] = new_data.data[date][
                            language
                        ]
            else:
                self.data[date] = new_data.data[date]

    def is_new_language(self, editor: EditorProcess) -> bool:
        if editor.language in self.data[self.day].keys():
            return True
        return False

    def add_language(self, editor: EditorProcess) -> None:
        language: str = editor.language
        start_time: float = editor.start_time
        current_time: float = time()
        self.data[self.day][language] = [start_time, current_time]

    def update_language(self, editor) -> None:
        language: str = editor.language
        start_time: float = self.data[self.day][language][0]
        current_time: float = time()
        self.data[self.day][language] = [start_time, current_time]

    def reset_data(self) -> None:
        self.data = {}
        self.data[self.day] = {}


class FileData:
    def __init__(self, path: str = "./data.dat"):
        self.path: str = path
        self.day_format: str = "%j %y"
        self.data: Data = None
        if os.path.exists(self.path):
            self.data = self.get_data_from_file()
        else:
            with open(self.path, "w") as f:
                f.write("{}")

    def get_data_from_file(self) -> Data:
        content: dict[str, dict[str, list[float]]] = {}
        with open(self.path, "r") as f:
            try:
                content = json.load(f)
            except json.decoder.JSONDecodeError:
                data: Data = Data()
                return Data()
        data = Data(content)
        return data

    def save(self, data: Data) -> None:
        data_dict: dict[str, dict[str, list[float]]] = data.data
        with open(self.path, "w") as f:
            json.dump(data_dict, f)

    def is_data(self) -> bool:
        with open(self.path, "r") as f:
            content = f.read()
        if len(content) > 2:
            return True
        return False

    def erase_data(self) -> None:
        with open(self.path, "w") as f:
            f.write("{}")
