"""

"""

import typing

import bs4
import requests


def get_soup(url: str) -> typing.Optional[bs4.BeautifulSoup]:
    """

    """
    res = requests.get(url)
    if res.status_code != 200:
        return None
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    return soup
