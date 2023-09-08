from datetime import date

import pytest

from codingTracker.process import EditorProcess, EditorTracker


@pytest.fixture
def ps_str() -> str:
    ps_entries = (
        "eguefif     33464  0.0  0.0  33464 11648 pts/1    T    06:46   0:55 vim client.py\n"
        "guefif     33  0.2  0.0  33 33516 pts/0    S+   05:05   3:15 vim test.c\n"
        "guefif     36  0.2  0.0  36 11648 pts/0    S+   12:33   12:05 nano test.cpp\n"
        "guefif     0  0.2  0.0  33111 11648 pts/0    S+   18:55   1:32 emacs test.xx\n"
        "guefif     22222  0.2  0.0  22222 11648 pts/0    S+   20:59  3:44 zoro test.js\n"
    )
    return ps_entries


def test_get_editors(ps_str: str) -> None:
    tracker: EditorTracker = EditorTracker()
    editor_list: list[EditorProcess] = tracker.get_editors(ps_str)
    assert len(editor_list) == 3
    assert editor_list[0].language == "python"
    assert editor_list[0].pid == 33464
    assert editor_list[0].time == 55
    assert editor_list[1].language == "c"
    assert editor_list[1].pid == 33
    assert editor_list[1].time == 195
    assert editor_list[2].language == "c++"
    assert editor_list[2].pid == 36
    assert editor_list[2].time == 725


editor_param = [
    (
        "eguefif     33464  0.0  0.0  33464 11648 pts/1    T    06:46   0:55 vim client.py",
        [33464, 55, "python", 1694083560.0],
    ),
    (
        "guefif     33  0.2  0.0  33 33516 pts/0    S+   05:05   3:15 vim test.c",
        [33, 195, "c", 1694077500.0],
    ),
    (
        "guefif     36  0.2  0.0  36 11648 pts/0    S+   12:33   12:05 nano test.cpp",
        [36, 725, "c++", 1694104380.0],
    ),
]


@pytest.mark.parametrize("value, expected", editor_param)
def test_editor_process(value, expected) -> None:
    today: date = date.fromisoformat("2023-09-07")
    editor: EditorProcess = EditorProcess(value, today)
    assert editor.pid == expected[0]
    assert editor.time == expected[1]
    assert editor.language == expected[2]
    assert editor.start_time == expected[3]


ps_entries_eq: list[tuple[str, str, bool]] = [
    (
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py",
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
        False,
    ),
    (
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
        True,
    ),
    (
        "eegu     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
        True,
    ),
]


@pytest.mark.parametrize("process1, process2, expected", ps_entries_eq)
def test_eq_(process1: str, process2: str, expected: str) -> None:
    assert (EditorProcess(process1) == EditorProcess(process2)) == expected
