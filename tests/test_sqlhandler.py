import os
import sqlite3

import pytest

from codingTracker.session import Session
from codingTracker.sqlhandler import SqlHandler


def test_sqlhandler_constructor_nofile() -> None:
    sql: SqlHandler = SqlHandler("./tests/db_test.db")

    curretval: sqlite3.Cursor = sql.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='sessions'"
    )
    table: tuple[str] = curretval.fetchone()

    assert os.path.isfile("./tests/db_test.db")
    assert len(table) == 1
    assert table[0] == "sessions"


def test_sqlhandler_constructor_file() -> None:
    sql: SqlHandler = SqlHandler("./tests/db_test.db")

    curretval: sqlite3.Cursor = sql.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='sessions'"
    )
    table: tuple[str] = curretval.fetchone()

    assert os.path.isfile("./tests/db_test.db")
    assert len(table) == 1
    assert table[0] == "sessions"


list_session: tuple[tuple[float, str], ...] = (
    (4314132.0, "python"),
    (3123124.0, "c"),
    (514131231.0, "c++"),
)

@pytest.fixture
def sessions() -> list[Session]:
    return [Session(s[0], s[1]) for s in list_session]


def test_sqlhandler_update(sessions) -> None:
    sql: SqlHandler = SqlHandler("./tests/db_test.db")
    sql.update(sessions)
    retval: sqlite3.Cursor
    values: list[tuple[str, float]]
    for s in list_session:
        retval = sql.cursor.execute(
            f"SELECT starttime, language FROM sessions WHERE startime={s[0]}"
        )
        values = retval.fetchall()
        assert len(values) == 1
        assert values[0][0] == s[0]
        assert values[0][1] == s[1]
