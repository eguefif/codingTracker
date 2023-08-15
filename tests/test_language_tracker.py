from time import struct_time, time, sleep

import pytest

from codingTracker.client import EditorProcess, ProcessTracker, Language, LanguageTracker

# Testing Languagetracker
@pytest.fixture
def list_editor_processes():
    ps_entries = [
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
def language_tracker():
    return LanguageTracker()

def test_update(list_editor_processes, language_tracker):
    language_tracker.update(list_editor_processes)
    assert len(language_tracker.language_list) == 4

@pytest.fixture()
def editor_list():
    editor_list = [
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    08:46   0:00 nano client.py",
        "guefif     1  0.2  0.0  33516 11648 pts/0    S+   09:05   0:00 vim test.py",
        "guefif     16  0.2  0.0  33516 11648 pts/0    S+   11:30   0:00 vim test.c",
        ]
    return editor_list

def test_get_data(editor_list):
    start = time()
    editor_process: List[EditorProcess] = [EditorProcess(process) for process in editor_list]
    tracker: LanguageTracker = LanguageTracker()
    tracker.update(editor_process)
    sleep(1)
    data: dict[str, int] = tracker.get_data()
    elasped_time = time() - start
    assert elasped_time - 0.1 < data["python"] < elasped_time 
    assert elasped_time - 0.1 < data["c"] < elasped_time 

# Testing Language class
@pytest.fixture
def python_editor_process():
    editor = EditorProcess(
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py")
    return editor

def test_language_constructor(python_editor_process):
    language = Language(python_editor_process)
    assert len(language.processes) == 1
    assert language.starting_time < time()
    assert language.name == "python"


@pytest.fixture
def list_python_editor_process():
    ps_entries = [
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py",
        "guefif     1  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        "guefif     16  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py",
        "eguefif     5535  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py",
        "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        "guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py",
        "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py",
        ]
    editor_list = [EditorProcess(entry) for entry in ps_entries]
    return editor_list

@pytest.fixture
def language_one():
    process = "eguefif     554  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py";
    editor = EditorProcess(process)
    language = Language(editor)
    return language

def test_add_language(list_python_editor_process: list[EditorProcess], language_one: Language):
    language_one.update(list_python_editor_process)
    assert len(language_one.processes) == 8

@pytest.fixture
def language_multiple():
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
    language.update(process[1:])
    return language

def test_remove_one_process(language_multiple, python_editor_process):
    language_multiple.remove_process(python_editor_process)
    assert len(language_multiple.processes) == 6

def test_remove_mutliple_test(language_multiple, list_python_editor_process):
    for process in list_python_editor_process[:2]:
        language_multiple.remove_process(process)

    assert len(language_multiple.processes) == 5

def test_is_process_here_true(language_multiple):
    process = EditorProcess(
            "guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py");
    assert language_multiple.is_process_here(process) == True

def test_is_process_here_false(language_multiple):
    process = EditorProcess(
            "eguefif     554  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py");
    assert language_multiple.is_process_here(process) == False

def test_remove_last_process():
    process = "eguefif     554  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py";
    editor = EditorProcess(process)
    language = Language(editor)
    sleep(1)
    language.remove_process(editor)
    assert len(language.processes) == 0
    assert 2 > language.time_spent > 1
