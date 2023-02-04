"""
API wrapper for MLB `league data`_.

.. _league data: https://statsapi.mlb.com/api/v1/league
"""

import dataclasses
import datetime

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
        cls.check_address_fields(fields)

        address = cls.base

        if fields.league_id is not None:
            address += f"/{fields.league_id}"

        address += "?"

        if fields.season is not None:
            address += f"season={fields.season}"

        return address


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


def latest_season(date: datetime.datetime = TODAY) -> int:
    """
    :param league:
    :param date:
    :return:
    """
    season_start = [
        AmericanLeague(date.year).data["leagues"][0]["seasonDateInfo"]["seasonStartDate"],
        NationalLeague(date.year).data["leagues"][0]["seasonDateInfo"]["seasonStartDate"]
    ]
    assert season_start[0] == season_start[1]

    dt_format = "%Y-%m-%d"
    start_date = datetime.datetime.strptime(season_start[0], dt_format)

    return date.year if date >= start_date else date.year - 1
