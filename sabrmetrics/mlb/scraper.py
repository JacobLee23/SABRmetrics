"""
"""

import typing

import bs4
import requests

from .address import APIAddress


class Scraper:
    """
    :param address:
    :param fields:
    """
    def __init__(self, address: APIAddress):
        self._address = address

        self._response = requests.get(
            self.address.url, params=self.address.parameters, timeout=100
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}(address={self.address})"

    @property
    def address(self) -> APIAddress:
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


class APIScraper(Scraper):
    """
    :param address:
    """
    def __init__(self, address: APIAddress):
        super().__init__(address)

        self._data = self.response.json()

    @property
    def data(self) -> dict:
        """
        :return:
        """
        return self._data


class WebScraper(Scraper):
    """
    :param address:
    """
    def __init__(self, address: APIAddress):
        super().__init__(address)

        self._soup = bs4.BeautifulSoup(self.response.text, features="lxml")

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """
        :return:
        """
        return self._soup