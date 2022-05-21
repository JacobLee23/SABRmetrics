"""

"""

import json
import os

import bs4
import requests


_HEADERS_PATH = os.path.join("data", "headers.json")
with open(_HEADERS_PATH, "r", encoding="utf-8") as file:
    HEADERS = json.load(file)


def get_soup(url: str) -> bs4.BeautifulSoup:
    """

    """
    res = requests.get(url, headers=HEADERS)
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    return soup
