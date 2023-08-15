from time import struct_time, time, sleep

import pytest

from codingTracker.client import EditorProcess, ProcessTracker, Language, LanguageTracker

# Test ProcessTracker
def get_editorprocesses_ps_entries():
    ps_entries = ""
    expected = []
    with open("./tests/ps_entries.dat", "r") as f:
        content = f.read()
    content = content.split("\n")
    idx = content.index("")
    for line in content[:idx]:
        ps_entries += line + "\n"
    expected = content[idx:]
    return ps_entries, expected

@pytest.fixture
def ps_list_str():
    ps_entries = "eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py\n" \
         "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py\n" \
         "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py\n" \
         "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.xx\n"
    return ps_entries

def test_get_editor_list(ps_list_str):
    tracker: ProcessTracker = ProcessTracker()
    print(ps_list_str)
    editor_list = tracker.get_editor_list(ps_list_str)
    print(editor_list)
    assert len(editor_list) == 3

def test_get_editor_processes():
    ps_entry, expected = get_editorprocesses_ps_entries()
    tracker = ProcessTracker()
    list_editors = tracker.get_editor_processes(ps_entry)
    for process in list_editors:
        assert process in expected

#Testing EditorProcess
ps_entries = [
    ("eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py", 5534),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py", 5541),
    ("guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py", 0),
    ("guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py", 11),
    ("eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 nano client.py", 5534),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py", 5541),
    ("guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py", 0),
    ("guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano test.py", 11),
    ("eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py", 5534),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py", 5541),
    ("guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py", 0),
    ("guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py", 11),
    ]

@pytest.mark.parametrize("ps_entry, expected", ps_entries)
def test_get_pid(ps_entry, expected):
    process = EditorProcess(ps_entry)
    assert process.pid == expected

ps_entries = [
    ("eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py", "python"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.c", "c"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim petachnock_salut.h", "c"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testCamel.hpp", "c++"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim TESTHTTPCamel.cpp", "c++"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspace .js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim tests pace.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim  testspace.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim 712test78 .js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test-spe.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspe-.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim -testspe.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test,spe.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim ,testspe.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspe,.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test(spe.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspe(.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim (testspe.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test)spe.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim )testspe.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim testspe).js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 nano )testspe.js", "javascript"),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs testspe).js", "javascript"),
    ]

@pytest.mark.parametrize("ps_entry, expected", ps_entries)
def test_get_language(ps_entry, expected):
    process = EditorProcess(ps_entry)
    assert process.language == expected

ps_entries= [
        ("eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 emacs client.py",
    "guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
        False),
    ("guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
    "guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 emacs test.py",
    True),
    ]

@pytest.mark.parametrize("process1, process2, expected", ps_entries)
def test_eq_(process1, process2, expected):
    assert (EditorProcess(process1) == EditorProcess(process2)) == expected
