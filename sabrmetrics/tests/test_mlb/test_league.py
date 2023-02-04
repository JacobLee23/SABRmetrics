"""
"""

import datetime
import urllib.request

import pytest
import requests

from sabrmetrics import TODAY
from sabrmetrics.mlb import league


class TestAddress:
    """
    Unit tests for :py:class:`league.Address`.
    """
    def test_default(self):
        """
        Unit test for :py:meth:`league.Address.default`.
        """
        with urllib.request.urlopen(league.Address.default()) as response:
            assert response.code == 200


@pytest.mark.parametrize(
    "x", [
        league.AmericanLeague(), league.NationalLeague(),
        league.CactusLeague(), league.GrapefruitLeague()
    ]
)
class TestLeague:
    """
    Unit tests for :py:class:`league.League`.
    """
    def test_address(self, x: league.League):
        """
        Unit test for :py:attr:`league.League.address`.
        """
        assert isinstance(x.address, str), x.address

        with urllib.request.urlopen(x.address) as response:
            assert response.code == 200, x.address

    def test_response(self, x: league.League):
        """
        Unit test for :py:attr:`league.League.response`.
        """
        assert isinstance(x.response, requests.Response)

        assert x.response.status_code == 200

    def test_data(self, x: league.League):
        """
        Unit test for :py:attr:`league.League.data`.
        """
        mlb_leagues = {
            league.AmericanLeague: ("American League", "AL"),
            league.NationalLeague: ("National League", "NL"),
            league.CactusLeague: ("Cactus League", "CL"),
            league.GrapefruitLeague: ("Grapefruit League", "GL")
        }
        assert isinstance(x, tuple(mlb_leagues))

        assert isinstance(x.data, dict)
        assert isinstance(x.data["leagues"], list) and len(x.data["leagues"]) == 1
        assert isinstance(x.data["leagues"][0], dict)
        assert all(isinstance(k, str) for k in x.data["leagues"][0])

        assert x.data["leagues"][0]["id"] == x.league_id
        assert int(x.data["leagues"][0]["season"]) == x.season
        assert x.data["leagues"][0]["link"] in x.address
        assert x.data["leagues"][0]["active"]

        for k, v in mlb_leagues.items():
            if isinstance(x, k):
                assert x.data["leagues"][0]["name"] == v[0]
                assert x.data["leagues"][0]["abbreviation"] == v[1]


@pytest.mark.parametrize(
    "season", range(2000, TODAY.year + 1)
)
def test_league_all_data(season: int):
    """
    Unit test for :py:meth:`league.League.all_data`.
    """
    x = league.League.all_data(season)

    assert isinstance(x, dict)
    assert isinstance(x["leagues"], list) and x["leagues"]
    assert all(isinstance(v, dict) for v in x["leagues"])
    assert all(isinstance(k, str) for v in x["leagues"] for k in v)


class TestSeason:
    """
    Unit tests for :py:class:`league.Season`.
    """


@pytest.mark.parametrize(
    "date, res", [
        (datetime.datetime(TODAY.year - 1, 1, 1), TODAY.year - 2),
        (datetime.datetime(TODAY.year - 1, 12, 31), TODAY.year - 1),
        (datetime.datetime(TODAY.year, 1, 1), TODAY.year - 1),
        (datetime.datetime(TODAY.year, 12, 31), TODAY.year)
    ]
)
def test_season_latest(date: datetime.datetime, res: int):
    """
    Unit test for :py:func:`league.latest_season`.
    """
    assert league.latest_season(date) == res, date
