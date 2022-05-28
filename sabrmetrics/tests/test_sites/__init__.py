"""

"""

import os


PLAYERS_PATH = os.path.join(
    "sabrmetrics", "tests", "test_sites", "players.txt"
)
with open(PLAYERS_PATH, "r", encoding="utf-8") as file:
    PLAYERS = file.read().split("\n")
