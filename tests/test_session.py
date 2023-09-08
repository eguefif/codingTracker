from datetime import date
from time import sleep, time

import pytest

from codingTracker.process import EditorProcess
from codingTracker.session import Session, SessionTracker


def test_data_update_endtime() -> None:
    session: Session = Session(333333333.0, "Python")
    now = time()
    session.update_endtime()
    assert round(session.end_time) == round(now)


today: date = date.today()


@pytest.fixture
def processes1() -> list[EditorProcess]:
    ps_entries: list[str] = [
        "eguefif     33464  0.0  0.0  33464 11648 pts/1    T    06:06   3:25 vim client.py",
        "guefif     33  0.2  0.0  33 33516 pts/0    S+   12:05   4:12 vim test.c",
        "guefif     22222  0.2  0.0  22222 11648 pts/0    S+   15:12   0:55 emacs test.js",
    ]
    retval = [EditorProcess(entry, today) for entry in ps_entries]
    return retval


@pytest.fixture
def processes2() -> list[EditorProcess]:
    ps_entries: list[str] = [
        "eguefif     33464  0.0  0.0  33464 11648 pts/1    T    06:06   3:25 vim client.py",
        "guefif     33  0.2  0.0  33 33516 pts/0    S+   12:05   4:12 vim test.c",
        "guefif     22222  0.2  0.0  22222 11648 pts/0    S+   06:46   0:00 emacs test.cpp",
    ]
    retval = [EditorProcess(entry, today) for entry in ps_entries]
    return retval


@pytest.fixture
def sessions() -> list[Session]:
    session1: Session = Session(33333333, "python")
    session2: Session = Session(55555555.0, "c")
    session3: Session = Session(65555555.0, "c")
    session3.running = False
    return [session1, session2, session3]


def test_active_sessions(sessions: list[Session]) -> None:
    sessiontracker: SessionTracker = SessionTracker()
    sessiontracker.data = sessions
    assert sessiontracker.active_sessions() == 2


@pytest.fixture
def sessiontracker(processes1) -> SessionTracker:
    data: SessionTracker = SessionTracker()
    data.update(processes1)
    return data


def test_sessiontracker_update(sessiontracker, processes2) -> None:
    sleep(1)
    now = round(time())
    sessiontracker.update(processes2)
    assert sessiontracker.active_sessions() == 3
    assert sessiontracker.data[0].start_time < sessiontracker.data[0].end_time
    assert round(sessiontracker.data[0].end_time) == now
    assert sessiontracker.data[0].language == "python"
    assert sessiontracker.data[3].language == "c++"
