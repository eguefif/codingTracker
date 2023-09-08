from time import time

import pytest

from codingTracker.process import EditorProcess
from codingTracker.session import Session, SessionTracker


def test_data_update_endtime() -> None:
    session: Session = Session(333333333.0, "Python")
    now = time()
    session.update_endtime()
    assert round(session.end_time) == round(now)


@pytest.fixture
def processes1() -> list[EditorProcess]:
    ps_entries: list[str] = [
        "eguefif     33464  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py",
        "guefif     33  0.2  0.0  33 33516 pts/0    S+   06:46   0:00 vim test.c",
        "guefif     22222  0.2  0.0  22222 11648 pts/0    S+   06:46   0:00 emacs test.js",
    ]
    retval = [EditorProcess(entry) for entry in ps_entries]
    return retval

@pytest.fixture
def processes2() -> list[EditorProcess]:
    ps_entries: list[str] = [
        "eguefif     33464  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py",
        "guefif     33  0.2  0.0  33 33516 pts/0    S+   06:46   0:00 vim test.c",
        "guefif     22222  0.2  0.0  22222 11648 pts/0    S+   06:46   0:00 emacs test.cpp",
    ]
    retval = [EditorProcess(entry) for entry in ps_entries]
    return retval

@pytest.fixture
def sessiontracker(processes1) -> SessionTracker:
    data: SessionTracker = SessionTracker()
    data.update(processes1)
    return data

def test_sessiontracker_update(sessiontracker, processes2) -> None:
    sessiontracker.update(processes2)
    pass
