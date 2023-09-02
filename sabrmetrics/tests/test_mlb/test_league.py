"""
Unit tests for :py:mod:`sabrmetrics.mlb.league`.
"""

import urllib.request

import pytest
import requests

from sabrmetrics.mlb import league
from sabrmetrics.mlb.address import APIAddress


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
        assert isinstance(x["leagues"], list) and len(x["leagues"]) == 1
        assert isinstance(x["leagues"][0], dict)
        assert all(isinstance(k, str) for k in x["leagues"][0])

        assert x["leagues"][0]["link"] in x.address.url
        assert x["leagues"][0]["active"]

        for k, v in mlb_leagues.items():
            if isinstance(x, k):
                assert x["leagues"][0]["name"] == v[0]
                assert x["leagues"][0]["abbreviation"] == v[1]
