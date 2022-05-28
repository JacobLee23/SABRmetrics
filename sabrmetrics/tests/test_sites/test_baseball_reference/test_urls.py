"""

"""

import string
import urllib.request

import pytest

from sabrmetrics.sites.baseball_reference import _urls
from sabrmetrics.tests.test_sites import _PLAYERS_PATH


with open(_PLAYERS_PATH, "r", encoding="utf-8") as file:
    PLAYERS = file.read().split("\n")


class TestURLs:
    """

    """
    urls = _urls.URLs()

    def test_base_address(self):
        with urllib.request.urlopen(self.urls.base_address) as res:
            assert res.getcode() == 200

    def test_base_url(self):
        with urllib.request.urlopen(self.urls.base_url) as res:
            assert res.getcode() == 200

    @pytest.mark.parametrize(
        "letter", string.ascii_lowercase
    )
    def test_player_index(self, letter: str):
        with urllib.request.urlopen(
                self.urls.player_index.format(letter=letter)
        ) as res:
            assert res.getcode() == 200

    @pytest.mark.parametrize(
        "letter,player_id", [
            (x[0], x) for x in PLAYERS
        ]
    )
    def test_player(self, letter: str, player_id: str):
        with urllib.request.urlopen(
                self.urls.player.format(letter=letter, player_id=player_id)
        ) as res:
            assert res.getcode() == 200
