from time import struct_time

import pytest

from codingTracker.client import VimProcess, CodingTracker

#Testing CodingTracker



#Testing VimProcess
ps_entries = [
    ("eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:46   0:00 vim client.py", 5534),
    ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py", 5541),
    ("guefif     0  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py", 0),
    ("guefif     11  0.2  0.0  33516 11648 pts/0    S+   06:46   0:00 vim test.py", 11),
    ]

@pytest.mark.parametrize("ps_entry, expected", ps_entries)
def test_get_pid(ps_entry, expected):
    process = VimProcess(ps_entry)
    assert process.pid == expected

ps_entries = [
        ("eguefif     5534  0.0  0.0  33464 11648 pts/1    T    06:47   0:00 vim client.py",
            struct_time((0, 0, 0, 6, 47, 0, 0, None, -1))),
        ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   12:23   0:00 vim test.py", 
            struct_time((0, 0, 0, 12, 23, 0, 0, None, -1))),
        ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   00:00   0:00 vim test.py", 
            struct_time((0, 0, 0, 0, 0, 0, 0, None, -1))),
        ("guefif     5541  0.2  0.0  33516 11648 pts/0    S+   24:59   0:00 vim test.py", 
            struct_time((0, 0, 0, 24, 59, 0, 0, None, -1))),
    ]

@pytest.mark.parametrize("ps_entry, expected", ps_entries)
def test_get_start_time(ps_entry, expected):
    process = VimProcess(ps_entry)
    assert process.start_time == expected

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
    ]

@pytest.mark.parametrize("ps_entry, expected", ps_entries)
def test_get_language(ps_entry, expected):
    process = VimProcess(ps_entry)
    assert process.language == expected
