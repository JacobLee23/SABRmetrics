"""
"""

import urllib.request

import pytest
import requests

from sabrmetrics.mlb import league


def test_base_address():
    """
    Unit test for :py:data:`league.BASE_ADDRESS`
    """
    with urllib.request.urlopen(league.BASE_ADDRESS) as response:
        assert response.code == 200


def test_leagues():
    """
    Unit test for :py:func:`league.leagues`.
    """


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
        assert isinstance(x.data["leagues"], list)
        assert len(x.data["leagues"]) == 1
        assert isinstance(x.data["leagues"][0], dict)
        assert all(isinstance(k, str) for k in x.data["leagues"][0])

        assert x.data["leagues"][0]["id"] == x.league_id
        assert x.data["leagues"][0]["link"] in x.address
        assert x.data["leagues"][0]["active"]

        for k, v in mlb_leagues.items():
            if isinstance(x, k):
                assert x.data["leagues"][0]["name"] == v[0]
                assert x.data["leagues"][0]["abbreviation"] == v[1]
