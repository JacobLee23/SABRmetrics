"""
Tests for :py:mod:`sabrmetrics.mlb.standings`.
"""


import pytest
import requests

from sabrmetrics.mlb import standings


@pytest.mark.parametrize(
    "x", [
        standings.RegularSeason()
    ]
)
class TestRegularSeason:
    """
    Tests for :py:class:`sabrmetrics.mlb.standings.RegularSeason`.
    """
    def test_base_address(self, x: standings.RegularSeason):
        """
        Unit test for :py:attr:`sabrmetrics.mlb.standings.RegularSeason.base_address`.
        """
        with requests.get(x.base_address) as response:
            assert response.status_code == 200, x.base_address

    def test_address(self, x: standings.RegularSeason):
        """
        Unit test for :py:attr:`sabrmetrics.mlb.standings.RegularSeason.address`.
        """
        with requests.get(x.address) as response:
            assert response.status_code == 200, x.address
