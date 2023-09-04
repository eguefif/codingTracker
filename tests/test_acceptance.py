import json
import subprocess
from multiprocessing import Process
from time import sleep, strftime, time


def run_client() -> None:
    subprocess.run(["codingTracker"])


def run_server() -> None:
    subprocess.run(["codingTrackerServer"])


def run_editor() -> None:
    subprocess.run(["vim", "test_lg.py"])


def test_acceptance_always_connected() -> None:
    with open("./data_server.dat", "w") as f:
        f.write("{}")
    start_time: float = time()
    client: Process = Process(target=run_client)
    server: Process = Process(target=run_server)
    # editor: Process = Process(target=run_editor)
    client.start()
    server.start()
    # editor.start()
    sleep(3)
    client.join(timeout=1)
    server.join(timeout=1)
    # editor.join(timeout=1)
    end_time: float = time()
    sleep(1)
    today: str = strftime("%j %y")
    test_dict: dict[str, dict[str, list[float]]] = {
        today: {"python": [round(start_time), round(end_time)]}
    }
    with open("./data_server.dat", "r") as f:
        content: dict[str, dict[str, list[float]]] = json.load(f)
    print(content)
    print(test_dict)
    assert content == test_dict
