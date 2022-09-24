"""

"""


import bs4
import requests


class RegularSeason:
    """

    """
    base_address = "https://mlb.com/standings"

    def __init__(self):
        self._address = self.base_address

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
        return requests.get(self.address)

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """

        :return:
        """
        return bs4.BeautifulSoup(self.response.text, features="lxml")
