"""

"""

import re
import string
import urllib.request

import pytest

from sabrmetrics.sites.baseball_reference import players
from sabrmetrics.tests.test_sites import PLAYERS


@pytest.mark.parametrize(
    "player_index", [players.PlayerIndex(x) for x in string.ascii_lowercase]
)
class TestPlayerIndex:
    """

    """
    def test_base_address(self, player_index: players.PlayerIndex):
        """

        """
        assert player_index.base_address
        assert [
                   x for _, x, _, _ in string.Formatter().parse(player_index.base_address) if x
               ][0] == "letter"

    def test_letter(self, player_index: players.PlayerIndex):
        """

        """
        assert player_index.letter.islower()
        assert player_index.letter in string.ascii_lowercase

    def test_url(self, player_index: players.PlayerIndex):
        """

        """
        with urllib.request.urlopen(player_index.url) as res:
            assert res.getcode() == 200

    def test_soup(self, player_index: players.PlayerIndex):
        """

        """
        assert player_index.soup

    def test_n_players(self, player_index: players.PlayerIndex):
        """

        """
        assert len(player_index.soup.select("div#players__sh")) == 1
        container = player_index.soup.select_one("div#players__sh")
        assert len(container.select("h2")) == 1
        elem = container.select_one("h2")
        assert elem.text
        assert re.search(r"\d+", elem.text.strip()) is not None

        assert isinstance(player_index.n_players(), int)
        assert player_index.n_players() >= 1

    def test_players(self, player_index: players.PlayerIndex):
        """

        """
        assert len(player_index.soup.select("div#div_players_")) == 1
        container = player_index.soup.select_one("div#div_players_")

        assert container.select("p")
        for elem in container.select("p"):
            assert len(elem.select("a")) == 1
            assert elem.select_one("a").text
            assert elem.text
            assert re.search(r"\d{4}", elem.text) is not None
            assert len(re.findall(r"\d{4}", elem.text)) == 2
            assert len(elem.select("b")) in (0, 1)
            assert elem.select_one("a").attrs.get("href") is not None


@pytest.mark.parametrize(
    "player", [players.Player(x) for x in PLAYERS]
)
class TestPlayers:
    """

    """
