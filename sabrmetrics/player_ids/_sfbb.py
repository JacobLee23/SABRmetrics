"""

"""

import json
import os
import typing

import bs4
import requests


_HEADERS_PATH = os.path.join("sabrmetrics", "player_ids", "data", "headers.json")
with open(_HEADERS_PATH, "r", encoding="utf-8") as file:
    HEADERS = json.load(file)


def get_soup(url: str) -> bs4.BeautifulSoup:
    """

    """
    res = requests.get(url, headers=HEADERS)
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    return soup


class SFBBTools:
    """

    """
    _base_address = "https://www.smartfantasybaseball.com/tools/"

    _primary_container_css = "div.entry-content > div > table tr:nth-child(2) > td:first-child"

    class URLs(typing.NamedTuple):
        """

        """
        excel_download: str
        web_view: str
        csv_download: str

        changelog_web_view: str
        changelog_csv_download: str

    @property
    def base_address(self) -> str:
        """

        """
        return self._base_address

    @property
    def _soup(self) -> bs4.BeautifulSoup:
        """

        """
        return get_soup(self.base_address)

    @property
    def _primary_container(self) -> bs4.Tag:
        """

        """
        container = self._soup.select_one(self._primary_container_css)
        return container

    @property
    def urls(self) -> URLs:
        """

        """
        hrefs = (e.attrs.get("href") for e in self._primary_container.select("a"))
        return self.URLs(*hrefs)
