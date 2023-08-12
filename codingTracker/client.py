from typing import List
import subprocess
import re
from time import struct_time, time

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


def get_vim_processes(processes: List[str]) -> List[str]:
    vim_processes = []
    for process in processes:
        if process.find("vim") != -1:
            vim_processes.append(process)
    return vim_processes


def main() -> None:
    vim_processes_list: List[VimProcess] = []
    retval: subprocess.CompletedProcess = subprocess.run(
        ["ps", "-aux"], capture_output=True, text=True
    )
    processes: List[str] = retval.stdout.split("\n")
    vim_processes: List[str] = get_vim_processes(processes)

    for process in vim_processes:
        vim_processes_list.append(VimProcess(process))

    for vim_process in vim_processes_list:
        print(
            vim_process.pid,
            vim_process.language,
            f"{vim_process.start_time.tm_hour}:{vim_process.start_time.tm_min}",
        )
