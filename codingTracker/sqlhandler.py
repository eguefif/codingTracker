import sqlite3

from codingTracker.session import Session


class SqlHandler:
    def __init__(self, database: str = "./client_database.db"):
        self.con: sqlite3.Connection = sqlite3.connect(database)
        self.cursor: sqlite3.Cursor = self.con.cursor()
        curretval: sqlite3.Cursor = self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='sessions'"
        )
        table: tuple[str] = curretval.fetchone()
        if table is None:
            self.cursor.execute(
                "CREATE TABLE sessions ("
                "language VARCHAR(50), start_time FLOAT, end_time FLOAT, running BOOL)"
            )

    def update(self, sessions: list[Session]) -> None:
        for session in sessions:
            retcur: sqlite3.Cursor = self.cursor.execute(
                f"SELECT * FROM sessions WHERE start_time={session.start_time}"
            )
            values: tuple[float] = retcur.fetchone()
            if values is None:
                self._insert(session)
            else:
                self._update_row(session)
        self.con.commit()

    def _insert(self, session: Session) -> None:
        self.cursor.execute(
            "INSERT INTO sessions (language, start_time, end_time, running)"
            "VALUES (:language, :start_time, :end_time, :running)",
            (
                {
                    "language": session.language,
                    "start_time": session.start_time,
                    "end_time": session.end_time,
                    "running": session.running,
                }
            ),
        )

    def _update_row(self, session: Session) -> None:
        self.cursor.execute(
            "UPDATE sessions SET end_time=:end_time, running=:running WHERE start_time=:start_time",
            (
                {
                    "end_time": session.end_time,
                    "running": session.running,
                    "start_time": session.start_time,
                }
            ),
        )

    def get_data(self) -> list[tuple[str, float, float, bool]]:
        retcur: sqlite3.Cursor = self.cursor.execute(
                "SELECT * FROM sessions"
                )
        return retcur.fetchall()

    def terminate(self) -> None:
        self.con.close()

    def delete(self) -> None:
        self.cursor.execute("DROP TABLE sessions")
        self.con.commit()
