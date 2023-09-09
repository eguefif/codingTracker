from ipaddress import ip_address, IPv4Address
from typing import Callable
import json

setup_dict: dict[str, str | int] = {
    "sleeping_time": 5,
    "ip": "127.0.0.1",
    "port": 10000,
    "path": "./data.dat",
    "encoding": "utf-8",
}

def check_ip(ip: str) -> str:
    if type(ip) is IPv4Address:
        return ip
    print("IP is not valid, default value is used")
    return setup_dict["ip"]

def check_sleeping(s: str) -> int:
    if s.isnumeric:
        return int(s)
    print("Sleeping time is not valid, default value is used")
    return setup_dict["sleeping_time"]

def check_port(s: str) -> int:
    if s.isnumeric and port < 65535:
        return int(s)
    print("Port is not valid, default value is used")
    return setup_dict["port"]

def check_encoding(s: str) -> str:
    encodings = ["utf-8", "utf-16"]
    if s in encodings:
        return s
    print("Port is not valid, default value is used")
    return setup_dict["encoding"]

def setup() -> None:
    questions: list[list[str, str, Callable]] = [
        [f"How often do you want the tracker to monitor and save your activity in seconds({setup_dict['sleeping_time']}): ", "sleeping_time", check_sleeping],
        [f"What is the server ip address({setup_dict['ip']}): ", "ip", check_ip],
        [f"What is the server port({setup_dict['port']}): ", "port", check_port],
        [f"What is the file path({setup_dict['path']}): ", "path", str],
        [f"What is the encoding your want to use ({setup_dict['encoding']}): ", "encoding", check_encoding],
    ]
    for question in questions:
        print(question[0], end="")
        retval: str = input()
        if retval != "":
            setup_dict[question[1]] = question[2](retval)


    with open("client.cfg", "w") as f:
        json.dump(setup_dict, f)


def main() -> None:
    setup()


if __name__ == "__main__":
    setup()
