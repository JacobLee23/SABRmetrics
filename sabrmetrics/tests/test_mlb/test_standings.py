"""
Tests for :py:mod:`sabrmetrics.mlb.standings`.
"""

import datetime

import pytest
import requests

from sabrmetrics.mlb import standings


TODAY = datetime.date.today()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TOMORROW = TODAY + datetime.timedelta(days=1)


@pytest.mark.parametrize(
    "x", [
        standings.RegularSeason(),
        standings.RegularSeason(date=YESTERDAY),
        standings.RegularSeason(year=1901),
        *[standings.RegularSeason(year=x) for x in [1955, 1959, 1963, 1965, 1981, 2020]],
        standings.RegularSeason(year=TODAY.year),
        *[standings.RegularSeason(group=x) for x in standings.RegularSeason._groups.values()],
        *[standings.RegularSeason(level=x) for x in standings.RegularSeason._levels.values()]
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

    def test_response(self, x: standings.RegularSeason):
        """
        Unit test for :py:attr:`sabrmetrics.mlb.standings.RegularSeason.response`.
        """
        assert x.response.status_code == 200

    def test_soup(self, x: standings.RegularSeason):
        """
        Unit test for :py:attr:`sabrmetrics.mlb.standings.RegularSeason.soup`.
        """
        assert x.soup
        assert x.soup.select_one("html")
