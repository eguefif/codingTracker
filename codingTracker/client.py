import signal
from time import sleep

from codingTracker.data import Data, FileData
from codingTracker.language import LanguageTracker
from codingTracker.process import EditorProcess, ProcessTracker
from codingTracker.connexion import DataHandler


class App:
    def __init__(self, sleeping_time: int = 5):
        self.sleeping_time = sleeping_time
        self.language_tracker: LanguageTracker = LanguageTracker()
        self.data: Data = Data()
        self.file_handler: FileData = FileData(nodata=False, path="./data.dat")
        self.process_tracker: ProcessTracker = ProcessTracker()
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        self.running: bool = True

    def run(self):
        while self.running:
            editor_processes: list[
                EditorProcess
            ] = self.process_tracker.get_processes()
            self.language_tracker.update(editor_processes)
            new_data = self.language_tracker.get_data()
            self.data.update(new_data)
            self.save_data()
            self.sleep()

    def sleep(self):
        sleep(self.sleeping_time)

    def save_data(self):
        self.file_handler.save(self.data.data)

    def signal_handler(self, sig, frame):
        if sig == signal.SIGINT or sig == signal.SIGTERM:
            self.save_data()
            self.connexion.terminate()
            self.running = False


def main() -> None:
    app = App()
    app.run()
