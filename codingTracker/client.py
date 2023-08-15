import re
import subprocess
from time import sleep, time, strftime, strptime, localtime
from typing import List
import json


LANGUAGES = {
    "": "None",
    "py": "python",
    "c": "c",
    "cpp": "c++",
    "hpp": "c++",
    "h": "c",
    "js": "javascript",
}


EDITORS = ("vim", "emacs", "nano")


class EditorProcess:
    def __init__(self, ps_entry: str):
        self.ps_entry: str = ps_entry
        self.pid: int = self.get_pid()
        self.language: str = self.get_language().strip()
        self.start_time: float = self.get_start_time()

    def get_pid(self) -> int:
        retval = re.search(r"\b[0-9]+\b", self.ps_entry)
        if retval is not None:
            return int(retval.group())
        return -1

    def get_language(self) -> str:
        editor_file: re.Match
        for editor in EDITORS:
            editor_file = re.search(
                f"(?<={editor}) *[a-zA-Z0-9.,-_() /]+", self.ps_entry
            )
            if isinstance(editor_file, re.Match):
                break
        if editor_file is not None:
            extension = self.get_extension(editor_file.group())
            if extension in LANGUAGES.keys():
                return LANGUAGES[extension]
        return "None"

    def get_extension(self, extension) -> str:
        idx = extension.find(".")
        if idx != -1:
            idx += 1
            return extension[idx:]
        else:
            return ""

    def get_start_time(self):
        """
        start_time = re.search(
            r"\b[0-2][0-9]:[0-9][0-9]\b", self.ps_entry
        ).group()
        s_time = struct_time(
            (0, 0, 0, int(start_time[0:2]), int(start_time[3:]), 0, 0, None, -1)
        )
        """
        return time()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EditorProcess):
            return NotImplemented
        return self.pid == other.pid

    def __repr__(self):
        retval = (
            f"pid: {self.pid}, language: {self.language},"
            "start time: {self.start_time}"
        )
        return retval


class ProcessTracker:
    def __init__(self):
        pass

    def get_processes(self) -> List[EditorProcess]:
        processes: subprocess.CompletedProcess = None
        editor_list: List[EditorProcess] = []

        processes = subprocess.run(
            ["ps", "-aux"], capture_output=True, text=True
        )
        editor_list = self.get_editor_list(processes.stdout)
        return editor_list

    def get_editor_list(self, processes: str) -> List[EditorProcess]:
        editor_list: List[EditorProcess] = []
        for process in self.get_editor_processes(processes):
            editor_process: EditorProcess = EditorProcess(process)
            if editor_process.language != "None":
                editor_list.append(editor_process)
        return editor_list

    def get_editor_processes(self, process_list: str) -> List[str]:
        processes: List[str] = []
        editor_processes: List[str] = []

        processes = process_list.split("\n")
        for process in processes:
            for editor in EDITORS:
                if process.find(editor) != -1:
                    editor_processes.append(process)
        return editor_processes


class Language:
    def __init__(self, process: EditorProcess = None) -> None:
        self.name: str = process.language
        self.starting_time: float = process.start_time
        self.time_spent: float = 0
        self.processes: List[EditorProcess] = []
        self.add_process_to_list(process)

    def update(self, editor_list: List[EditorProcess]) -> None:
        for process in editor_list:
            if not process in self.processes:
                self.append_process(editor)
        for process in self.processes:
            if process not in editor_list:
                self.processes.pop(process)

    def append_process(self, process: EditorProcess) -> None:
        if not len(self.processes):
            self.starting_time = time()
        self.processes.append(process)

    def remove_process(self, process: EditorProcess) -> None:
        if self.is_process_here(process):
            self.processes.remove(process)
        if not len(self.processes):
            self.time_spent += time() - self.starting_time
            self.starting_time = 0

    def get_time_spent(self) -> float:
        if len(self.processes) > 0:
            return int(time() - self.starting_time)
        else:
            return self.time_spent

    def __str__(self):
        retval = (
            f"Language: {self.name}, starting_time: {self.starting_time},"
            "Number of processes: {len(self.processes)}"
        )
        return retval


class LanguageTracker:
    def __init__(self) -> None:
        self.language_list: List[Language] = []

    def update(self, editor_list: List[EditorProcess]) -> None:
        self.update_languages(editor_list)
        self.update_process_list(editor_list)

    def update_languages(self, editor_list: List[EditorProcess]) -> None:
        for editor in editor_list:
            if self.is_new_language(editor):
                self.add_new_language_to_list(editor)
            else:
                for language in self.language_list:
                    language.update(editor_list)

    def is_new_language(self, editor: EditorProcess) -> bool:
        for language in self.language_list:
            if language.name == editor.language:
                return False
        return True

    def add_new_language_to_list(self, editor: EditorProcess) -> None:
        language = Language(editor)
        self.language_list.append(language)

    def get_data(self) -> dict[str, int]:
        data: dict[str, int] = {}
        for lg in self.language_list:
            data[lg.name] = lg.get_time_spent()
        return data

    def __str__(self):
        retval = "\n".join([str(lg) for lg in self.language_list])
        return retval


class DataProcessing:
    def __init__(self, remote: bool = False, local: bool = True, file: str = "./data.dat"):
        self.remote: bool = remote
        self.local: bool = local
        self.file = file
        self.day_format = "%j %y"
        self.data: dict[str, int] = self.get_data_from_file()

    def get_data_from_file(self) -> dict[str, int]:
        content: dict[str, dict[str, int]] = {}
        day: str = ""

        with open(self.file, "r") as f:
            content = json.load(f)
        day = strftime(self.day_format, localtime())
        for key, value in content.items():
            if (key == day):
                return value
        return {}

    def update_data(self, new_data:dict[str, int]) -> None:
        for key, value in new_data.items():
            self.data[key] = value
        self.save()

    def save(self) -> None:
        day = strftime(self.day_format, localtime())
        with open(self.file, 'r') as f:
            content = json.load(f)
        if day in content.keys():
            for key, value in self.data.items():
                if key in content[day].keys():
                    content[day][key] += self.data[key]
                else:
                    content[day][key] = self.data[key]
        else:
            content[day] = self.data
        with open(self.file, 'w') as f:
            json.dump(content, f)


class App:
    def __init__(self, sleeping_time: int = 5):
        self.sleeping_time = 5
        self.language_tracker: LanguageTracker = LanguageTracker()
        self.process_tracker: ProcessTracker = ProcessTracker()
        self.editor_list: List[EditorProcess] = []
        self.data_processing: DataProcessing = DataProcessing()

    def run(self):
        while True:
            self.editor_list = self.process_tracker.get_processes()
            self.language_tracker.update(self.editor_list)
            data = self.language_tracker.get_data()
            self.data_processing.update_data(data)
            sleep(self.sleeping_time)


def main() -> None:
    app = App()
    app.run()
