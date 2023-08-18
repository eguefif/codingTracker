from time import sleep, time
from typing import List

import pytest

from codingTracker.language import Language, LanguageTracker
from codingTracker.process import EditorProcess


# Testing Languagetracker
@pytest.fixture
def list_editor_processes() -> list[EditorProcess]:
    ps_entries: list[str] = [
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py",
        "guefif     1  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        "guefif     16  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.c",
        "eguefif     5535  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.cpp",
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.cpp",
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        "guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.js",
        "eguefif     5538  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.c",
        "eguefif     5532  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py",
    ]
    editor_list = [EditorProcess(entry) for entry in ps_entries]
    return editor_list


@pytest.fixture
def tracker():
    return LanguageTracker()


def test_update(
    list_editor_processes: list[EditorProcess], tracker: LanguageTracker
) -> None:
    tracker.update(list_editor_processes)
    assert len(tracker.language_list) == 4
    for lg in tracker.language_list:
        if lg.name == "python":
            assert len(lg.processes) == 4
        elif lg.name == "c":
            assert len(lg.processes) == 2
        elif lg.name == "cpp":
            assert len(lg.processes) == 3
        elif lg.name == "javascript":
            assert len(lg.processes) == 1
    list_editor_processes.pop()
    list_editor_processes.pop()
    tracker.update(list_editor_processes)
    assert len(tracker.language_list) == 4
    for lg in tracker.language_list:
        if lg.name == "python":
            assert len(lg.processes) == 3
        elif lg.name == "c":
            assert len(lg.processes) == 1
        elif lg.name == "cpp":
            assert len(lg.processes) == 3
        elif lg.name == "javascript":
            assert len(lg.processes) == 1


def test_get_data(list_editor_processes, tracker) -> None:
    start = time()
    tracker.update(list_editor_processes)
    sleep(1)
    data: dict[str, int] = tracker.get_data()
    elasped_time = time() - start
    assert elasped_time - 0.1 < data["python"] < elasped_time
    assert elasped_time - 0.1 < data["c"] < elasped_time
    assert elasped_time - 0.1 < data["javascript"] < elasped_time
    assert elasped_time - 0.1 < data["c++"] < elasped_time


# Testing Language class
@pytest.fixture
def python_editor_process() -> EditorProcess:
    editor = EditorProcess(
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py"
    )
    return editor


@pytest.fixture
def one_language_editor_list() -> List[EditorProcess]:
    ps_entries = [
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py",
        "guefif     1  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        "guefif     16  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py",
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.cpp",
        "eguefif     5535  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py",
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        "guefif     554  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        "guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.c",
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.js",
    ]
    editor_list = [EditorProcess(entry) for entry in ps_entries]
    return editor_list


@pytest.fixture
def one_language_object() -> Language:
    process = "eguefif     554  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py"
    editor = EditorProcess(process)
    language = Language(editor)
    return language


def test_add_process(
    one_language_editor_list: list[EditorProcess], one_language_object: Language
):
    one_language_object.update(one_language_editor_list)
    assert len(one_language_object.processes) == 7


@pytest.fixture
def language_multiple():
    editor: list[EditorProcess]
    processes = [
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py",
        "guefif     1  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        "guefif     16  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        "eguefif     5535  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py",
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        "guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
    ]
    editor = [EditorProcess(process) for process in processes]
    language = Language(editor[0])
    language.update(editor[1:])
    return language


def test_language_constructor(python_editor_process: EditorProcess) -> None:
    language = Language(python_editor_process)
    assert len(language.processes) == 1
    assert language.starting_time < time()
    assert language.name == "python"


def test_remove_one_process(language_multiple: Language) -> None:
    process = "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py"
    editor = EditorProcess(process)
    language_multiple.remove_process(editor)
    assert len(language_multiple.processes) == 6


def test_remove_one_process_not_in_list(language_multiple: Language) -> None:
    process = "eguefif     4  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py"
    editor = EditorProcess(process)
    language_multiple.remove_process(editor)
    assert len(language_multiple.processes) == 6


def test_remove_multiple(
    language_multiple: Language,
    one_language_editor_list: List[EditorProcess],
) -> None:
    for process in one_language_editor_list[:2]:
        language_multiple.remove_process(process)
    assert len(language_multiple.processes) == 5


def test_remove_last_process() -> None:
    process = "eguefif     554  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py"
    editor = EditorProcess(process)
    language = Language(editor)
    sleep(1)
    language.remove_process(editor)
    sleep(1)
    assert len(language.processes) == 0
    assert 1.1 > language.time_spent > 1
