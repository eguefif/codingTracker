import json


def setup() -> None:
    setup_dict: dict[str, str | int] = {
        "sleeping_time": 5,
        "ip": "127.0.0.1",
        "port": 10000,
        "path": "./data.dat",
        "encoding": "utf-8",
    }
    print("Welcome to codingTracker setup app")
    print("Do you want to setup a server or a client(client): ", end="")
    choice: str = input()
    if choice == "client":
        print(
            "How often do you want the tracker to monitor and "
            f"save your activity in seconds({setup_dict['sleeping_time']}): ",
            end="",
        )
    setup_dict["sleeping_time"] = int(input())
    print(f"What is the server ip address({setup_dict['ip']}): ", end="")
    setup_dict["ip"] = input()
    print(f"What is the server port({setup_dict['port']}): ", end="")
    setup_dict["port"] = int(input())
    print(f"What is the file path({setup_dict['path']}): ", end="")
    setup_dict["path"] = input()
    print(
        f"What is the encoding your want to use ({setup_dict['encoding']}): ",
        end="",
    )
    setup_dict["encoding"] = input()
    if choice == "client":
        path: str = "./client.cfg"
    else:
        path = "./server.cfg"
    with open(path, "w") as f:
        json.dump(setup_dict, f)


def main() -> None:
    setup()


if __name__ == "__main__":
    setup()
