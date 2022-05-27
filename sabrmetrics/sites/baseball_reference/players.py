"""

"""

import re
import string
import typing

import bs4
import pandas as pd

from . import _urls
from .._scrape import get_soup


_URLS = _urls.URLs()


class PlayerIndex:
    """

    """
    _base_address = _URLS.player_index

    def __init__(self, letter: str):
        if letter not in string.ascii_letters:
            raise ValueError(letter)
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
            years = tuple(map(int, re.findall(r"\d{4}", elem.text)))[:2]
            active = elem.select_one("b") is not None
            hof = "+" in elem.text
            href = _URLS.base_address + elem.select_one("a").attrs.get("href")

            yield self._Player(
                name=name, years=years, active=active, hof=hof, href=href
            )


class Player:
    """

    """
    _base_address = _URLS.player

    def __init__(self, player_id: str):
        """

        """
        self._player_id = player_id.lower()
        self._letter = self.player_id[0]

        self._soup = get_soup(self.url)

    class _Meta(typing.NamedTuple):
        """

        """
        name: str
        position: str
        bats: str
        throws: str

        height: tuple[int, int]


    class _Jersey(typing.NamedTuple):
        """

        """
        number: int
        team: str
        years: tuple[int]

    @property
    def base_address(self) -> str:
        """

        """
        return self._base_address

    @property
    def player_id(self) -> str:
        """

        """
        return self._player_id

    @property
    def letter(self) -> str:
        """

        """
        return self._letter

    @property
    def url(self) -> str:
        """

        """
        return _URLS.player.format(letter=self.letter, id=self.player_id)

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """

        """
        return self._soup

    def meta(self):
        """

        """

    def accolades(self) -> typing.Optional[typing.Tuple[str]]:
        """

        """
        container = self.soup.select_one("div#info > ul#bling")
        if container is None:
            return None

        res = []
        for elem in container.select("li > a"):
            res.append(str(elem.text).strip())

        return tuple(res)

    def jerseys(self) -> typing.Tuple[_Jersey]:
        """

        """
        container = self.soup.select_one("div#info > div.uni_holder.br")

        res = []
        for elem in container.select("a.poptip"):
            number = int(elem.select_one("svg > text").text.strip())
            team = re.search(
                r"^\d{4}-\d{4} (.*)$", elem.attrs.get("data-tip").strip()
            ).group(1)
            years = tuple(
                map(int, re.findall(r"\d{4}", elem.attrs.get("data-tip")))
            )[:2]

            res.append(
                self._Jersey(number=number, team=team, years=years)
            )

        return tuple(res)

    def stats_pullout(self) -> pd.DataFrame:
        """

        """
        container = self.soup.select_one("div#info > div.stats_pullout")
        df_ = pd.DataFrame(
            columns=[
                x.text.strip() for x in container.select("span.poptip > strong")
            ],
            index=[
                x.text.strip() for x in container.select("div:nth-child(1) > div > p > strong")
            ]
        )

        for i, elem in enumerate(container.select("div.p1 > div, div.p2 > div, div.p3 > div")):
            df_.iloc[:, i] = list(map(float, (e.text.strip() for e in elem.select("p"))))

        return df_
