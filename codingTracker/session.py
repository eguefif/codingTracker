from time import strftime, time

from codingTracker.process import EditorProcess


class Session:
    def __init__(
        self, start_time: float, language: str, day_format: str = "%j %y"
    ):
        self.language = language
        self.start_time: float = start_time
        self.end_time: float = start_time + 0.1
        self.day = strftime(day_format)
        self.running = True

    def update_endtime(self) -> None:
        self.end_time = time()


class SessionTracker:
    def __init__(self) -> None:
        self.data: list[Session] = []

    def update(self, editors: list[EditorProcess]) -> None:
        self._running_editors(editors)
        self._ending_session(editors)

    def _running_editors(self, editors: list[EditorProcess]) -> None:
        for editor in editors:
            if self._is_new_language(editor.language):
                self._add_language(editor)
            else:
                self._update_language(editor)

    def _is_new_language(self, language: str) -> bool:
        for session in self.data:
            if session.language == language:
                return False
        return True

    def _add_language(self, editor: EditorProcess) -> None:
        new_session: Session = Session(editor.start_time, editor.language)
        self.data.append(new_session)

    def _update_language(self, editor: EditorProcess) -> None:
        for session in self.data:
            if session.language == editor.language:
                session.update_endtime()
                break

    def _ending_session(self, editors) -> None:
        for session in self.data:
            if not self._language_in(session.language, editors):
                session.running = False

    def _language_in(self, language: str, editors: list[EditorProcess]) -> bool:
        for editor in editors:
            if editor.language == language:
                return True
        return False
