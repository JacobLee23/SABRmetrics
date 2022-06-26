"""

"""

import datetime
import re
import string
import urllib.request

import bs4
import pandas as pd
import pytest

from sabrmetrics.sites.baseball_reference import players
from sabrmetrics.tests.test_sites.test_baseball_reference import BATTERS, PITCHERS, PLAYERS


@pytest.mark.parametrize(
    "player_index", [players.PlayerIndex(x) for x in string.ascii_lowercase]
)
class TestPlayerIndex:
    """

    """
    def test_base_address(self, player_index: players.PlayerIndex):
        """

        """
        assert [
                   x for _, x, _, _ in string.Formatter().parse(player_index.base_address) if x
               ] == ["letter"]

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
    def test_base_address(self, player: players.Player):
        """

        """
        assert [
                   x for _, x, _, _ in string.Formatter().parse(player.base_address) if x
               ] == ["letter", "player_id"]

    def test_player_id(self, player: players.Player):
        """

        """
        assert player.player_id.islower() and player.player_id.isalnum()
        assert re.search(r"^[a-z]{,7}[0-9]{,2}$", player.player_id) is not None

    def test_letter(self, player: players.Player):
        """

        """
        assert player.letter in string.ascii_lowercase
        assert player.letter.islower()
        assert player.letter == player.player_id[0]

    def test_url(self, player: players.Player):
        """

        """
        with urllib.request.urlopen(player.url) as res:
            assert res.getcode() == 200

    def test_soup(self, player: players.Player):
        """

        """
        assert player.soup

    def test_meta(self, player: players.Player):
        """

        """
        assert len(player.soup.select("div#info > div#meta")) == 1
        container = player.soup.select_one("div#info > div#meta")
        assert len(container.select("div > h1 > span")) == 1
        assert container.select_one("div > h1 > span").text
        assert len(container.select("div.media-item.multiple > img")) >= 1
        assert all(
            e.attrs.get("src") is not None
            for e in container.select("div.media-item.multiple > img")
        )
        assert container.select("div > p")
        assert all(e.text for e in container.select("div > p"))

        meta = player.meta()
        assert all(meta._asdict().values())

    def test_accolades(self, player: players.Player):
        """

        """

    def test_jerseys(self, player: players.Player):
        """

        """
        assert len(player.soup.select("div#info > div.uni_holder.br")) == 1
        container = player.soup.select_one("div#info > div.uni_holder.br")
        for elem in container.select("a.poptip"):
            assert len(elem.select("svg > text")) == 1
            assert elem.select_one("svg > text").text
            assert elem.attrs.get("data-tip") is not None
            assert re.search(r"^\d{4}-\d{4} (.*)$", elem.attrs.get("data-tip")) is not None
            assert len(re.findall(r"\d{4}", elem.attrs.get("data-tip"))) == 2

        jerseys = player.jerseys()
        assert all(all(x._asdict().values()) for x in jerseys)

    def stats_pullout(self, player: players.Player):
        """

        """
        assert len(self.soup.select("div#info > div.stats-pullout")) == 1
        container = self.soup.select_one("div#info > div.stats_pullout")
        assert container.select("span.poptip > strong")
        a = container.select("span.poptip > strong")
        assert container.select("div:nth-child(1) > div > p > strong")
        b = container.select("div:nth-child(1) > div > p > strong")
        assert len(a) == len(b)
        assert all(e.text for e in a)
        assert all(e.text for e in b)

        assert all(
            len(container.select(x)) == 1
            for x in ("div.p1 > div", "div.p2 > div", "div.p3 > div")
        )
        for elem in container.select("div.p1 > div, div.p2 > div, div.p3 > div"):
            assert elem.select("p")
            assert len(elem.select("p")) == len(a) == len(b)
            assert all(e.text for e in elem.select("p"))

        stats = player.stats_pullout()
        assert len(stats.index) in (1, 2)
        assert set(stats.index) in (
            {"Career"},
            {str(datetime.datetime.now().year), "Career"}
        )


@pytest.mark.parametrize(
    "overview", [players._BattingOverview(x) for x in BATTERS]
)
class TestOverview:
    """

    """
    def test_player_id(self, overview: players._BattingOverview):
        """

        """
        assert overview.player_id.islower() and overview.player_id.isalnum()
        assert re.search(r"^[a-z]{,7}[0-9]{,2}$", overview.player_id) is not None

    def test_letter(self, overview: players._BattingOverview):
        """

        """
        assert overview.letter in string.ascii_lowercase
        assert overview.letter.islower()
        assert overview.letter == overview.player_id[0]

    def test_url(self, overview: players._BattingOverview):
        """

        """
        with urllib.request.urlopen(overview.url) as res:
            assert res.getcode() == 200

    def test_response(self, overview: players._BattingOverview):
        """

        """
        assert overview.response.status_code == 200

    def test_soup(self, overview: players._BattingOverview):
        """

        """
        assert overview.soup
        for name, css in overview._css.items():
            if name in (
                "Postseason Batting",
                "Similarity Scores",
                "Salaries"
            ):
                continue
            assert len(overview.soup.select(css)) == 1, name

    def test_tables(self, overview: players._BattingOverview):
        """

        """
        for name, css in overview._css.items():
            if name in (
                "Postseason Batting",
                "Similarity Scores",
                "Salaries"
            ):
                continue

            elem = overview.soup.select_one(css)
            if "commented" not in elem.attrs.get("class"):
                assert elem.select_one("table") is not None, name
            else:
                assert (
                    x := elem.findAll(string=lambda s: isinstance(s, bs4.Comment))
                ), name
                assert bs4.BeautifulSoup(
                    x[0], features="lxml"
                ).select_one("table") is not None, name

    def test_standard_batting(self, overview: players._BattingOverview):
        """

        """
        assert "Standard Batting" in overview.tables

        data = overview.standard_batting()

    def test_player_value(self, overview: players._BattingOverview):
        """

        """
        assert "Player Value" in overview.tables

        data = overview.player_value()

    def test_advanced_batting(self, overview: players._BattingOverview):
        """

        """
        assert "Advanced Batting" in overview.tables

        df = overview.tables.get("Advanced Batting")
        assert isinstance(df.columns, pd.MultiIndex)

        data = overview.advanced_batting()

    def test_postseason_batting(self, overview: players._BattingOverview):
        """

        """
        assert "Postseason Batting" in overview.tables
        if overview.tables.get("Postseason Batting") is None:
            return

        data = overview.postseason_batting()

    def test_standard_fielding(self, overview: players._BattingOverview):
        """

        """
        assert "Standard Fielding" in overview.tables

        data = overview.standard_fielding()

    def test_appearances(self, overview: players._BattingOverview):
        """

        """
        assert "Appearances" in overview.tables

        data = overview.appearances()

    def test_leaderboard(self, overview: players._BattingOverview):
        """

        """
        assert "Leaderboard" in overview.tables

        container = overview.soup.select_one(
            overview._css.get("Leaderboard")
        ).find(string=lambda s: isinstance(s, bs4.Comment))
        assert container
        soup_ = bs4.BeautifulSoup(container, features="lxml")

        assert soup_.select("table > caption")
        titles = [x.text for x in soup_.select("table > caption")]
        assert all(titles)
        dfs = pd.read_html(container)

        data = overview.leaderboard()

        assert len(titles) == len(dfs) == len(data)

    def test_hall_of_fame_statistics(self, overview: players._BattingOverview):
        """

        """
        assert "Hall of Fame Statistics" in overview.tables

    def test_similarity_scores(self, overview: players._BattingOverview):
        """

        """
        assert "Similarity Scores" in overview.tables

    def test_salaries(self, overview: players._BattingOverview):
        """

        """
        assert "Salaries" in overview.tables
