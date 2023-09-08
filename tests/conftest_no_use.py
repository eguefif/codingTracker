import pytest
from time import strftime

from codingTracker.connexion import Connexion
from codingTracker.data import Data

DAY_FORMAT: str = "%j %y"

@pytest.fixture(scope="module")
def connexion() -> Connexion:
    return Connexion()

@pytest.fixture(scope="module")
def data_day_object() -> Data:
    day: str = strftime(DAY_FORMAT)
    data_dict: dict[str, dict[str, list[float]]] = {
        day: {
            "python": [21.12, 41.23],
            "javascript": [21.12, 41.23],
            "c++": [21.12, 41.23],
            "c": [21.12, 41.2],
        },
        "110 2023": {
            "python": [21.12, 41.23],
            "javascript": [21.12, 41.23],
            "c": [21.12, 41.2],
        },
        "111 2023": {
            "python": [21.12, 41.23],
            "javascript": [21.12, 41.23],
            "c": [21.12, 41.2],
        },
    }
    data: Data = Data(data_dict)
    return data
