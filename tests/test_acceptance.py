import json
import pytest
import multiprocessing
import subprocess
from time import time, strftime

from codingTracker.client import App as clientApp
from codingTracker.server import App as serverApp


def test_acceptance_always_connected() -> None:
    start_time: float = time()
    end_time: float = time()
    today: str = strftime("%j %y")
    test_dict: dict[str, dict[str, list[float]]] = {today: {"python": [round(start_time), round(end_time)]}}
    with open("./data_server.dat", "r") as f:
        content: dict[str, dict[str, list[float]]] = json.load(f)
    assert content == test_dict
