"""
API wrapper for MLB `league data`_.

.. _league data: https://statsapi.mlb.com/api/v1/league
"""

import datetime

import requests


BASE_ADDRESS = "https://statsapi.mlb.com/api/v1/league"

CURRENT_YEAR = datetime.datetime.today().year


def concatenate_url(league_id: int = None, season: int = None):
    address = BASE_ADDRESS

    if league_id is not None and isinstance(league_id, int):
        address += f"/{league_id}"

    address += "?"

    if season is not None and isinstance(season, int):
        address += f"season={season}"

    return address


class League:
    """
    :param league_id:
    :param season:
    """
    def __init__(self, league_id: int, season: int):
        self._league_id, self._season = int(league_id), int(season)

        self._address = concatenate_url(self.league_id, self.season)
        self._response = requests.get(self.address)
        self._data = self.response.json()

    @classmethod
    def all_data(cls, season: int) -> dict:
        """
        :param season:
        """
        address = concatenate_url(season=season)

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
    def __init__(self, season: int = CURRENT_YEAR):
        super().__init__(103, season)


class NationalLeague(League):
    """
    :param season:
    """
    def __init__(self, season: int = CURRENT_YEAR):
        super().__init__(104, season)


class CactusLeague(League):
    """
    :param season:
    """
    def __init__(self, season: int = CURRENT_YEAR):
        super().__init__(114, season)


class GrapefruitLeague(League):
    """
    :param season:
    """
    def __init__(self, season: int = CURRENT_YEAR):
        super().__init__(115, season)
