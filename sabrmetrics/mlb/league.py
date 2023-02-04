"""
"""

import requests


def leagues(season: int) -> dict:
    """
    """
    address = f"https://statsapi.mlb.com/api/v1/league?season={season}"

    with requests.get(address) as response:
        return response.json()


class League:
    """
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
        """
        return self._league_id

    @property
    def season(self) -> int:
        """
        """
        return self._season

    @property
    def address(self) -> str:
        """
        """
        return self._address

    @property
    def response(self) -> requests.Response:
        """
        """
        return self._response

    @property
    def data(self) -> dict:
        """
        """
        return self._data


class AmericanLeague(League):
    """
    """
    def __init__(self, season: int):
        super().__init__(103, season)


class NationalLeague(League):
    """
    """
    def __init__(self, season: int):
        super().__init__(104, season)
