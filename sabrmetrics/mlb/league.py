"""
"""

import datetime
import typing

import requests

from .address import Address_
from .scraper import APIScraper
from sabrmetrics import TODAY


class Address(Address_):
    """
    """
    base = "https://statsapi.mlb.com/api/v1/league"

    class _FieldDefaults(typing.NamedTuple):
        """
        """
        league_id: int = None
        season: int = TODAY.year

    def concatenate(self) -> str:
        fpath = []
        if self["league_id"] is not None:
            fpath.append(str(self["league_id"]))

        queries = {}
        if self["season"] is not None:
            queries.setdefault("season", str(self["season"]))

        return f"{self.base}/{'/'.join(fpath)}?{'&'.join(f'{k}={v}' for k, v in queries.items())}"


class League(APIScraper):
    """
    :param league_id:
    :param season:
    """
    def __init__(self, league_id: int, season: int):
        kwargs = {}
        kwargs.setdefault("league_id", int(league_id))
        kwargs.setdefault("season", int(season))
        
        super().__init__(Address(**kwargs))

    @classmethod
    def all_data(cls, season: int) -> dict:
        """
        :param season:
        """
        address = Address(season=season)
        url = address.concatenate()

        with requests.get(url) as response:
            return response.json()


class AmericanLeague(League):
    """
    :param season:
    """
    def __init__(self, season: int = TODAY.year):
        super().__init__(103, season)


class NationalLeague(League):
    """
    :param season:
    """
    def __init__(self, season: int = TODAY.year):
        super().__init__(104, season)


class CactusLeague(League):
    """
    :param season:
    """
    def __init__(self, season: int = TODAY.year):
        super().__init__(114, season)


class GrapefruitLeague(League):
    """
    :param season:
    """
    def __init__(self, season: int = TODAY.year):
        super().__init__(115, season)


class Season:
    """
    """
    def __init__(self, year: int = TODAY.year):
        self._year = year

        league_data = (
            AmericanLeague(year).data["leagues"][0],
            NationalLeague(year).data["leagues"][0]
        )
        assert league_data[0]["seasonDateInfo"] == league_data[1]["seasonDateInfo"]

        self._data = league_data[0]["seasonDateInfo"]

    def __getitem__(self, key: str) -> typing.Union[int, float, str, datetime.datetime]:
        value = self.data[key]

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            pass

        return value

    @property
    def data(self) -> dict:
        """
        :return:
        """
        return self._data

    @property
    def year(self) -> int:
        """
        :return:
        """
        return self._year

    @classmethod
    def latest(cls, date: datetime.datetime = TODAY) -> "Season":
        """
        :param date:
        :return:
        """
        season = cls(TODAY.year)
        return season if date >= season["seasonStartDate"] else cls(date.year - 1)
