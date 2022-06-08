"""

"""

import datetime
import math
import re
import string
import typing

import bs4
import numpy as np
import pandas as pd
from playwright.sync_api import sync_playwright

from . import _urls
from .._scrape import get_soup


_URLS = _urls.URLs()


class PlayerIndex:
    """

    """
    _base_address = _URLS.player_index

    def __init__(self, letter: str):
        """
        :param letter:
        """
        if letter not in string.ascii_letters:
            raise ValueError(letter)
        self._letter = letter.lower()

        self._soup = get_soup(self.url)

    class _Player(typing.NamedTuple):
        """
        .. py:attribute:: name

        .. py:attribute:: year

        .. py:attribute:: active

        .. py:attribute:: hof

        .. py:attribute:: href
        """
        name: str
        years: tuple[int]
        active: bool
        hof: bool

        href: str

    @property
    def base_address(self) -> str:
        """
        :return:
        """
        return self._base_address

    @property
    def letter(self) -> str:
        """
        :return:
        """
        return self._letter

    @property
    def url(self) -> str:
        """
        :return:
        """
        return self.base_address.format(
            letter=self.letter
        )

    @property
    def soup(self) -> typing.Optional[bs4.BeautifulSoup]:
        """
        :return:
        """
        return self._soup

    def n_players(self) -> int:
        """
        :return:
        """
        container = self.soup.select_one("div#players__sh")
        elem = container.select_one("h2")

        return int(re.search(r"\d+", elem.text.strip()).group())

    def players(self) -> typing.Generator[_Player, None, None]:
        """
        :return:
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
        :param player_id:
        """
        self._player_id = player_id.lower()
        self._letter = self.player_id[0]

        self._soup = get_soup(self.url)

    class _Meta(typing.NamedTuple):
        """
        .. py:attribute:: name

        .. py:attribute:: src

        .. py:attribute:: content
        """
        name: str
        src: list[str]
        content: str

    class _Jersey(typing.NamedTuple):
        """
        .. py:attiribute:: number

        .. py:attribute:: team

        .. py:attribute:: years
        """
        number: int
        team: str
        years: tuple[int]

    @staticmethod
    def url_concat(letter: str, player_id: str) -> str:
        """

        """
        return _URLS.player.format(
            letter=letter,
            player_id=player_id
        )

    @property
    def base_address(self) -> str:
        """
        :return:
        """
        return self._base_address

    @property
    def player_id(self) -> str:
        """
        :return:
        """
        return self._player_id

    @property
    def letter(self) -> str:
        """
        :return:
        """
        return self._letter

    @property
    def url(self) -> str:
        """
        :return:
        """
        return self.url_concat(self.letter, self.player_id)

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """
        :return:
        """
        return self._soup

    def meta(self) -> _Meta:
        """
        :return:
        """
        container = self.soup.select_one("div#info > div#meta")

        name = container.select_one("div > h1 > span").text.strip()
        src = [
            e.attrs.get("src") for e in container.select("div.media-item.multiple > img")
        ]
        content = "\n".join(
            " ".join(e.text.strip().split()) for e in container.select("div > p")
        )

        return self._Meta(name=name, src=src, content=content)

    def accolades(self) -> typing.Optional[typing.Tuple[str]]:
        """
        :return:
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
        :return:
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
            )

            res.append(
                self._Jersey(number=number, team=team, years=years)
            )

        return tuple(res)

    def stats_pullout(self) -> pd.DataFrame:
        """
        :return:
        """
        container = self.soup.select_one("div#info > div.stats_pullout")
        df_ = pd.DataFrame(
            columns=[
                e.text.strip() for e in container.select("span.poptip > strong")
            ],
            index=[
                e.text.strip() for e in container.select("div:nth-child(1) > div > p > strong")
            ]
        )

        for i, elem in enumerate(container.select("div.p1 > div, div.p2 > div, div.p3 > div")):
            df_.iloc[:, i] = list(map(float, (e.text.strip() for e in elem.select("p"))))

        return df_


class _BattingOverview:
    """

    """
    _standard_batting = "div#content > div#all_batting_standard"

    def __init__(self, player_id: str):
        """
        :param player_id:
        """
        self._player_id = player_id
        self._letter = self.player_id[0]

        self._url = Player.url_concat(self.letter, self.player_id)

        with sync_playwright() as play:
            browser = play.chromium.launch()
            page = browser.new_page()

            page.goto(self.url, timeout=0)
            self._tables = pd.read_html(page.content())

            browser.close()

    class _StandardBatting(typing.NamedTuple):
        """

        """
        seasons: pd.DataFrame
        career: pd.Series
        season_average: pd.Series
        teams: pd.DataFrame = None
        leagues: pd.DataFrame = None

    @property
    def player_id(self) -> str:
        """
        :return:
        """
        return self._player_id

    @property
    def letter(self) -> str:
        """
        :return:
        """
        return self._letter

    @property
    def url(self) -> str:
        """
        :return:
        """
        return self._url

    @property
    def tables(self) -> list[pd.DataFrame]:
        """
        :return:
        """
        return self._tables

    def standard_batting(self, minors: bool = False) -> _StandardBatting:
        """
        :return:
        """
        df_ = self.tables[]     # FIXME

        if not minors:
            df_.drop(
                index=[
                    x for x in df_.index
                    if not math.isnan(df_.loc[x, "Tm"]) and "min" in df_.loc[x, "Tm"]
                ],
                inplace=True
            )

        dividers = [x for x in df_.index if df_.loc[x].isna().all()]
        if len(dividers) == 2:
            seasons, career, season_average, teams, leagues = (
                df_.loc[:dividers[0] - 3, :],
                df_.loc[(dividers[0] - 2), :],
                df_.loc[(dividers[0] - 1), :],
                df_.loc[(dividers[0] + 1):(dividers[1] - 1), :],
                df_.loc[(dividers[1] + 1):, :]
            )
        elif len(dividers) == 1:
            seasons, career, season_average, teams, leagues = (
                df_.loc[:dividers[0] - 3, :],
                df_.loc[(dividers[0] - 2), :],
                df_.loc[(dividers[0] - 1), :],
                df_.loc[(dividers[0] + 1):, :],
                None
            )
        else:
            seasons, career, season_average, teams, leagues = (
                df_.loc[:-3, :],
                df_.loc[-2, :],
                df_.loc[-1, :],
                None,
                None
            )

        seasons.drop(
            index=[x for x in seasons.index if "min" in seasons.loc[x, "Tm"]],
            inplace=True
        )
        seasons.loc[:, "Lg"] = seasons.loc[:, "Lg"].apply(
            lambda x: x.split(",")
        )
        seasons.loc[:, "Pos"] = seasons.loc[:, "Pos"].apply(
            lambda x: re.findall(r"[*/][0-9HD]", x) if not math.isnan(x) else np.nan
        )
        seasons.loc[:, "Awards"] = seasons.loc[:, "Awards"].apply(
            lambda x: np.nan if math.isnan(x) else (np.nan if "\xa0" in x else x.split(","))
        )

        career.drop(labels=["Pos", "Awards"], inplace=True)
        _add = {
            "Yrs": int(re.search(r"\d+", career.iloc[0]).group())
        }
        career = pd.concat([pd.Series(_add), career.iloc[4:]])

        season_average.drop(labels=["Pos", "Awards"], inplace=True)
        _add = {
            "Gms": int(re.search(r"\d+", season_average.iloc[0]).group())
        }
        season_average = pd.concat([pd.Series(_add), career.iloc[4:]])

        if teams is not None:
            teams.drop(columns=["Pos", "Awards"], inplace=True)
            _add = {
                "Tm": re.search(r"[A-Z]{3}", teams.iloc[0]).group(),
                "Yrs": int(re.search(r"\d+", teams.iloc[0]).group())
            }
            teams = pd.concat([pd.DataFrame(_add), teams])

        if leagues is not None:
            leagues.drop(columns=["Pos", "Awards"], inplace=True)
            _add = {
                "Lg": re.search(r"[A-Z]{2}", leagues.iloc[0]).group(),
                "Yrs": int(re.search(r"\d+", leagues.iloc[0]).group())
            }
            leagues = pd.concat([pd.DataFrame(_add), leagues])

        return self._StandardBatting(seasons, career, season_average, teams, leagues)
