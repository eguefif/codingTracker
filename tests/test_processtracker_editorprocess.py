from typing import List

import pytest

from codingTracker.client import EditorProcess, ProcessTracker


# Test ProcessTracker
@pytest.fixture
def editorprocesses_from_file() -> tuple[str, List[str]]:
    ps_entries: str = ""
    expected: List[str] = []
    content: str = ""
    with open("./tests/ps_entries.dat", "r") as f:
        content = f.read()
    content_list: List[str] = content.split("\n")
    idx: int = content_list.index("")
    for line in content_list[:idx]:
        ps_entries += line + "\n"
    expected = content_list[idx:]
    return ps_entries, expected


@pytest.fixture
def ps_list_str() -> List[str]:
    ps_entries = [
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py\n"
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py\n"
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py\n"
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.xx\n"
    ]
    return ps_entries


def test_get_editor_list(ps_list_str: List[str]) -> None:
    tracker: ProcessTracker = ProcessTracker()
    ps_str = "".join(ps_list_str)
    editor_list: List[EditorProcess] = tracker.get_editor_list(ps_str)
    assert len(editor_list) == 3


def test_get_editor_processes(
    editorprocesses_from_file: tuple[str, List[str]]
) -> None:
    ps_entry, expected = editorprocesses_from_file
    tracker: ProcessTracker = ProcessTracker()
    list_editors: List[str] = tracker.get_editor_processes(ps_entry)
    for process in list_editors:
        assert process in expected


# Testing EditorProcess
ps_entries_pid: List[tuple[str, int]] = [
    (
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py",
        5534,
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        5541,
    ),
    (
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        0,
    ),
    (
        "guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        11,
    ),
    (
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py",
        5534,
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        5541,
    ),
    (
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        0,
    ),
    (
        "guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        11,
    ),
    (
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py",
        5534,
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
        5541,
    ),
    (
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
        0,
    ),
    (
        "guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
        11,
    ),
]


@pytest.mark.parametrize("ps_entry, expected", ps_entries_pid)
def test_get_pid(ps_entry: str, expected: int) -> None:
    process: EditorProcess = EditorProcess(ps_entry)
    assert process.pid == expected


ps_entries: List[tuple[str, str]] = [
    (
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py",
        "python",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.c",
        "c",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim petachnock_salut.h",
        "c",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testCamel.hpp",
        "c++",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim TESTHTTPCamel.cpp",
        "c++",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspace .js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim tests pace.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim  testspace.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim 712test78 .js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test-spe.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspe-.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim -testspe.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test,spe.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim ,testspe.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspe,.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test(spe.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspe(.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim (testspe.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test)spe.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim )testspe.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspe).js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano )testspe.js",
        "javascript",
    ),
    (
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs testspe).js",
        "javascript",
    ),
]


@pytest.mark.parametrize("ps_entry, expected", ps_entries)
def test_get_language(ps_entry: str, expected: str) -> None:
    process: EditorProcess = EditorProcess(ps_entry)
    assert process.language == expected


ps_entries_eq: List[tuple[str, str, bool]] = [
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
]


@pytest.mark.parametrize("process1, process2, expected", ps_entries_eq)
def test_eq_(process1: str, process2: str, expected: str) -> None:
    assert (EditorProcess(process1) == EditorProcess(process2)) == expected
