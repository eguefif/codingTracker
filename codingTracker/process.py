import re
import subprocess
from datetime import date
from time import mktime

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
    def __init__(self, ps_entry: str, today: date = None):
        if today is None:
            today = date.today()
        self.ps_entry: str = ps_entry
        self.pid: int = self._get_pid()
        self.language: str = self._get_language().strip()
        self.start_time: float = self._get_start_time(today)
        self.time: int = self._get_time()

    def _get_pid(self) -> int:
        retval: re.Match = re.search(r"\b[0-9]+\b", self.ps_entry)
        if retval is not None:
            return int(retval.group())
        return -1

    def _get_language(self) -> str:
        editor_file: re.Match
        for editor in EDITORS:
            editor_file = re.search(
                f"(?<={editor}) *[a-zA-Z0-9.,-_() /]+", self.ps_entry
            )
            if isinstance(editor_file, re.Match):
                break
        if editor_file is not None:
            extension = self._get_extension(editor_file.group())
            if extension in LANGUAGES.keys():
                return LANGUAGES[extension]
        return "None"

    def _get_extension(self, extension) -> str:
        idx: int = extension.find(".")
        if idx != -1:
            idx += 1
            return extension[idx:]
        else:
            return ""

    def _get_start_time(self, today: date) -> float:
        time_str: str = self._get_times()[0]
        epoch: float = mktime(today.timetuple())
        hours: float = float(time_str[:2])
        minutes: float = float(time_str[3:])
        return epoch + hours * 3600 + minutes * 60

    def _get_time(self) -> int:
        split: list[str] = self._get_times()[1].split(":")
        hours: int = int(split[0])
        minutes: int = int(split[1])
        return hours * 60 + minutes

    def _get_times(self) -> list[str]:
        return re.findall(r"[0-9]*[0-9]:[0-9][0-9]", self.ps_entry)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EditorProcess):
            return NotImplemented
        return self.pid == other.pid

    def __repr__(self):
        retval = (
            f"Pid: {self.pid}, Language: {self.language},"
            f" Start time: {self.start_time},"
            f" Time: {self.time}"
        )
        return retval


class EditorTracker:
    def __init__(self):
        pass

    def get_editors(self, ps_stdout: str = None) -> list[EditorProcess]:
        if ps_stdout is None:
            ps_stdout = self._get_ps_output()
        editor_list: list[EditorProcess] = []
        for process in self._get_editor_processes(ps_stdout):
            editor_process: EditorProcess = EditorProcess(process)
            if editor_process.language != "None":
                editor_list.append(editor_process)
        return editor_list

    def _get_editor_processes(self, ps_stdout: str) -> list[str]:
        processes: list[str] = []
        editor_processes: list[str] = []

        self._get_ps_output()
        processes = ps_stdout.split("\n")
        for process in processes:
            for editor in EDITORS:
                if process.find(editor) != -1:
                    editor_processes.append(process)
        return editor_processes

    def _get_ps_output(self) -> str:
        processes: subprocess.CompletedProcess = None
        processes = subprocess.run(["ps", "-u"], capture_output=True, text=True)
        ps_stdout = processes.stdout
        return ps_stdout
