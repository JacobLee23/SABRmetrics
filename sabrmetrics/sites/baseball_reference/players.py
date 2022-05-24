"""

"""

import re
import string
import typing

import bs4

from . import _urls
from .._scrape import get_soup


_URLS = _urls.URLs()


class PlayerIndex:
    """

    """
    _base_address = _URLS.player_index

    def __init__(self, letter: str):
        if letter not in string.ascii_letters:
            raise ValueError

        self._letter = letter.lower()

        self._soup = get_soup(self.url)

    class _Player(typing.NamedTuple):
        """

        """
        name: str
        years: tuple[int]
        active: bool
        hof: bool

        href: str

    @property
    def base_address(self) -> str:
        """

        """
        return self._base_address

    @property
    def letter(self) -> str:
        """

        """
        return self._letter

    @property
    def url(self) -> str:
        """

        """
        return self.base_address.format(
            letter=self.letter
        )

    @property
    def soup(self) -> typing.Optional[bs4.BeautifulSoup]:
        """

        """
        return self._soup

    def n_players(self) -> int:
        """

        """
        container = self.soup.select_one("div#players__sh")
        elem = container.select_one("h2")

        return int(re.search(r"\d+", elem.text.strip()).group())

    def players(self) -> typing.Generator[_Player, None, None]:
        """

        """
        container = self.soup.select_one("div#div_players_")

        for elem in container.select("p"):
            name = elem.select_one("a").text
            years = tuple(map(int, re.findall(r"\d{4}", elem.text)))
            active = elem.select_one("b") is not None
            hof = "+" in elem.text
            href = _URLS.base_address + elem.select_one("a").attrs.get("href")

            yield self._Player(
                name=name, years=years, active=active, hof=hof, href=href
            )
