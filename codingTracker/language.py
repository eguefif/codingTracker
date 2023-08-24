from time import time
from codingTracker.process import EditorProcess, ProcessTracker

class Language:
    def __init__(self, process: EditorProcess = None) -> None:
        self.name: str = process.language
        self.starting_time: float = process.start_time
        self.time_spent: float = 0 
        self.processes: list[EditorProcess] = []
        self.append_process(process)

    def update(self, editor_list: list[EditorProcess]) -> None:
        for process in editor_list:
            if process.language == self.name:
                if process not in self.processes:
                    self.append_process(process)
        for process in self.processes:
            if process.language == self.name:
                if process not in editor_list:
                    self.remove_process(process)

    def append_process(self, process: EditorProcess) -> None:
        if not len(self.processes):
            self.starting_time = time()
        self.processes.append(process)

    def remove_process(self, process: EditorProcess) -> None:
        if process in self.processes:
            self.processes.remove(process)
        if not len(self.processes):
            self.time_spent += time() - self.starting_time
            self.starting_time = -1

    def get_time_spent(self) -> float:
        if len(self.processes):
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
        self.language_list: list[Language] = []

    def update(self, editor_list: list[EditorProcess]) -> None:
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

    def get_data(self) -> Data:
        day: str = strftime("%j %y")
        data_dict: dict[str, dict[str, int]] = {}
        for lg in self.language_list:
            data_dict[day][lg.name] = int(lg.get_time_spent())
        data: File = Data(data_dict)
        return data

    def __str__(self):
        retval = "\n".join([str(lg) for lg in self.language_list])
        return retval
