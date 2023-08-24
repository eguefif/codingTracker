import re
import subprocess
from time import time

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
        return time()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EditorProcess):
            return NotImplemented
        return self.pid == other.pid

    def __repr__(self):
        retval = (
            f"pid: {self.pid}, language: {self.language},"
            f"start time: {self.start_time}"
        )
        return retval


class ProcessTracker:
    def __init__(self):
        pass

    def get_processes(self) -> list[EditorProcess]:
        processes: subprocess.CompletedProcess = None
        editor_list: list[EditorProcess] = []

        processes = subprocess.run(["ps", "-u"], capture_output=True, text=True)
        editor_list = self.get_editor_list(processes.stdout)
        return editor_list

    def get_editor_list(self, processes: str) -> list[EditorProcess]:
        editor_list: list[EditorProcess] = []
        for process in self.get_editor_processes(processes):
            editor_process: EditorProcess = EditorProcess(process)
            if editor_process.language != "None":
                editor_list.append(editor_process)
        return editor_list

    def get_editor_processes(self, process_list: str) -> list[str]:
        processes: list[str] = []
        editor_processes: list[str] = []

        processes = process_list.split("\n")
        for process in processes:
            for editor in EDITORS:
                if process.find(editor) != -1:
                    editor_processes.append(process)
        return editor_processes
