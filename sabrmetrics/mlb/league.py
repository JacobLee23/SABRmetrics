"""
API wrapper for MLB `league data`_.

.. _league data: https://statsapi.mlb.com/api/v1/league
"""

import datetime

import requests


BASE_ADDRESS = "https://statsapi.mlb.com/api/v1/league"

CURRENT_YEAR = datetime.datetime.today().year


def leagues(season: int = CURRENT_YEAR) -> dict:
    """

    :param season:
    :return:
    """
    address = f"{BASE_ADDRESS}?season={season}"

    with requests.get(address) as response:
        return response.json()


class League:
    """
    :param league_id:
    :param season:
    """
    format_address = "https://statsapi.mlb.com/api/v1/league/{}?season={}"
    
    def __init__(self, league_id: int, season: int):
        self._league_id, self._season = int(league_id), int(season)

        self._address = self.format_address.format(self.league_id, self.season)
        self._response = requests.get(self.address)
        self._data = self.response.json()

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
