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
    def __init__(self, address: typing.Type[Address_], fields: Address_.Fields):
        self._fields = fields
        self._address = address.concatenate(fields)
        self._response = requests.get(self.address)
        self._soup = bs4.BeautifulSoup(self.response.text, features="lxml")
        self._data = self.response.json()

    @property
    def fields(self) -> Address_.Fields:
        """
        :return:
        """
        return self._fields

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


class APIScraper(Scraper):
    """
    :param address:
    :param fields:
    """
    def __init__(self, address: typing.Type[Address_], fields: Address_.Fields):
        super().__init__(address, fields)

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
    :param fields:
    """
    def __init__(self, address: typing.Type[Address_], fields: Address_.Fields):
        super().__init__(address, fields)

        self._soup = bs4.BeautifulSoup(self.response.text, features="lxml")

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """
        :return:
        """
        return self._soup