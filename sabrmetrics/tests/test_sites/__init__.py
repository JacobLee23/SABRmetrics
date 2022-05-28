"""

"""

import os

_DIRECTORY = os.path.join(
    "sabrmetrics", "tests", "test_sites", "test_baseball_reference"
)
BATTERS_PATH = os.path.join(_DIRECTORY, "test_batters.txt")
PITCHERS_PATH = os.path.join(_DIRECTORY, "test_pitchers.txt")

with open(BATTERS_PATH, "r", encoding="utf-8") as file:
    BATTERS = file.read().split("\n")
with open(PITCHERS_PATH, "r", encoding="utf-8") as file:
    PITCHERS = file.read().split("\n")
PLAYERS = BATTERS + PITCHERS
