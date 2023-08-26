from time import time
from codingTracker.process import EditorProcess, ProcessTracker

class LanguageTracker:
    def __init__(self, data) -> None:
        self.language_list: dict[str, [float, float]] = {}
        self.data: Data = data

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
