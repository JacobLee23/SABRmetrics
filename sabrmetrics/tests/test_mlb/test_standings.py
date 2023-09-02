"""
Unit tests for :py:mod:`sabrmetrics.mlb.standings`.
"""

import urllib.request

import pytest
import requests

from sabrmetrics.mlb import standings
from sabrmetrics.mlb.address import APIAddress


@pytest.mark.parametrize(
    "x", [
        standings.Standings()
    ]
)
class TestStandings:
    """
    Unit tests for :py:mod:`standings.Standings`.
    """
    def test_data(self, x: standings.Standings):
        """
        Unit tests for :py:attr:`standings.Standings.data`.
        """
