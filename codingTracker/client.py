import re
import subprocess
from time import struct_time, time
from typing import List

LANGUAGES = {
    "py": "python",
    "c": "c",
    "cpp": "c++",
    "hpp": "c++",
    "h": "c",
    "js": "javascript",
}


class VimProcess:
    def __init__(self, ps_entry: str):
        self.ps_entry: str = ps_entry
        self.pid: int = self.get_pid()
        self.language: str = self.get_language().strip()
        self.start_time: struct_time = self.get_start_time()

    def get_pid(self) -> int:
        retval = re.search(r"\b[0-9]+\b", self.ps_entry)
        if retval is not None:
            return int(retval.group())
        return -1

    def get_language(self) -> str:
        vim_file = re.search(r"(?<=vim)\s*[a-zA-Z0-9.,-_() ]+", self.ps_entry)
        if vim_file is not None:
            extension = self.get_extension(vim_file.group())
            return LANGUAGES[extension]
        else:
            return ""

    def get_extension(self, extension) -> str:
        idx = extension.find(".")
        if idx != -1:
            idx += 1
            return extension[idx:]
        else:
            return ""

    def get_start_time(self):
        start_time = re.search(
            r"\b[0-2][0-9]:[0-9][0-9]\b", self.ps_entry
        ).group()
        s_time = struct_time(
            (0, 0, 0, int(start_time[0:2]), int(start_time[3:]), 0, 0, None, -1)
        )
        return s_time


class Language:
    def __init__(self, vim_process: VimProcess):
        self.starting_time = time()
        self.vim_processes: list[VimProcess]
        self.vim_processes.append(vim_process)

    def append_process(self, vim_process: VimProcess) -> None:
        self.vim_processes.append(vim_process)


class CodingTracker:
    def __init__(self, refresh_time: int = 5):
        self.refresh_time: int = refresh_time
        self.vim_processes: List[VimProcess] = []

    def update(self) -> None:
        processes: subprocess.CompletedProcess = ""

        processes = subprocess.run(
            ["ps", "-aux"], capture_output=True, text=True
        )
        for process in self.get_vim_processes(processes):
            self.vim_processes.append(VimProcess(process))

    def get_vim_processes(self, processes: str) -> List[str]:
        processes = retval.stdout.split("\n")
        vim_processes = []
        for process in processes:
            if process.find("vim") != -1:
                vim_processes.append(process)
        return vim_processes


def main() -> None:
    app = CodingTracker()
    app.update()
