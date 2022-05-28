"""

"""

import os

_DIRECTORY = os.path.join(
    "sabrmetrics", "tests", "test_sites", "test_baseball_reference"
)
BATTERS_PATH = os.path.join(_DIRECTORY, "test_batters.txt")
PITCHERS_PATH = os.path.join(_DIRECTORY, "test_pitchers.txt")

with open(BATTERS_PATH, "r", encoding="utf-8") as file:
    BATTERS = [x for x in file.read().split("\n") if x]
with open(PITCHERS_PATH, "r", encoding="utf-8") as file:
    PITCHERS = [x for x in file.read().split("\n") if x]
PLAYERS = BATTERS + PITCHERS
