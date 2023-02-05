"""
"""

import dataclasses
import datetime
import typing

import requests

from .address import Address_
from sabrmetrics import TODAY


class Address(Address_):
    base = "https://statsapi.mlb.com/api/v1/league"

    @dataclasses.dataclass
    class Fields:
        """
        :param league_id:
        :param season:
        """
        league_id: int = None
        season: int = TODAY.year

    @classmethod
    def concatenate(cls, fields: Fields) -> str:
        """
        :param fields:
        :return:
        """
        cls.check_address_fields(fields)

        filepath = []
        if fields.league_id is not None:
            filepath.append(str(fields.league_id))

        queries = {}
        if fields.season is not None:
            queries.setdefault("season", str(fields.season))

        return f"{cls.base}{'/'.join(filepath)}?{'&'.join(f'='.join(x) for x in queries.items())}"


class League:
    """
    :param league_id:
    :param season:
    """
    def __init__(self, league_id: int, season: int):
        self._league_id, self._season = int(league_id), int(season)

        self._address = Address.concatenate(
            Address.Fields(self.league_id, self.season)
        )
        self._response = requests.get(self.address)
        self._data = self.response.json()

    @classmethod
    def all_data(cls, season: int) -> dict:
        """
        :param season:
        """
        address = Address.concatenate(
            Address.Fields(season=season)
        )

        with requests.get(address) as response:
            return response.json()

    @property
    def address(self) -> str:
        """
        :return:
        """
        return self._address

    @property
    def response(self) -> requests.Response:
        """
        :return:
        """
        return self._response

    @property
    def data(self) -> dict:
        """
        :return:
        """
        return self._data

    @property
    def league_id(self) -> int:
        """
        :return:
        """
        return self._league_id

    @property
    def season(self) -> int:
        """
        :return:
        """
        return self._season


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
