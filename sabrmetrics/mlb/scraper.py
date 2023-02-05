"""
"""

import typing

import bs4
import requests

from .address import Address_


class Scraper:
    """
    :param address:
    :param fields:
    """
    def __init__(self, address: Address_):
        self._address = address
        self._fields = self.address.fields
        self._url = self.address.concatenate()
        self._response = requests.get(self.url)

    @property
    def address(self) -> Address_:
        """
        :return:
        """
        return self._address

    @property
    def fields(self) -> typing.Dict[str, str]:
        """
        :return:
        """
        return self._fields

    @property
    def url(self) -> str:
        """
        :return:
        """
        return self._url

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
    def __init__(self, address: Address_):
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
    def __init__(self, address: Address_):
        super().__init__(address)

        self._soup = bs4.BeautifulSoup(self.response.text, features="lxml")

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """
        :return:
        """
        return self._soup