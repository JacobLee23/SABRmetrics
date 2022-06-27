"""

"""

import re
import string
import typing

import bs4
import numpy as np
import pandas as pd
import requests

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
    _css = {
        "Standard Batting": "div#all_batting_standard",
        "Player Value": "div#all_batting_value",
        "Advanced Batting": "div#all_batting_advanced",
        "Postseason Batting": "div#all_batting_postseason",
        "Standard Fielding": "div#all_standard_fielding",
        "Appearances": "div#all_appearances",
        "Leaderboard": "div#all_leaderboard",
        "Hall of Fame Statistics": "div#all_hof_other",
        "Salaries": "div#all_br-salaries"
    }

    def __init__(self, player_id: str):
        """
        :param player_id:
        """
        self._player_id = player_id
        self._letter = self.player_id[0]

        self._url = Player.url_concat(self.letter, self.player_id)

        self._response = requests.get(self.url)
        self._soup = bs4.BeautifulSoup(self.response.text, features="lxml")

        self._tables = self._scrape_tables()

    class _StandardBatting(typing.NamedTuple):
        """

        """
        seasons: pd.DataFrame
        career: pd.Series
        season_average: pd.Series
        teams: pd.DataFrame = None
        leagues: pd.DataFrame = None

    class _PlayerValue(typing.NamedTuple):
        """

        """
        seasons: pd.DataFrame
        career: pd.Series
        season_average: pd.Series
        teams: pd.DataFrame = None

    class _AdvancedBatting(typing.NamedTuple):
        """

        """
        seasons: pd.DataFrame
        career: pd.Series
        mlb_averages: pd.Series

    class _PostseasonBatting(typing.NamedTuple):
        """

        """
        seasons: pd.DataFrame
        career: pd.Series = None
        series_types: pd.Series = None

    class _StandardFielding(typing.NamedTuple):
        """

        """
        seasons: pd.DataFrame
        positions: pd.DataFrame

    class _Appearances(typing.NamedTuple):
        """

        """
        seasons: pd.DataFrame
        total: pd.Series

    class _Salaries(typing.NamedTuple):
        """

        """
        seasons: pd.DataFrame
        arbitration_eligible: int = None
        free_agent: int = None
        career_to_date: int = None

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
    def response(self) -> requests.Response:
        """
        :return:
        """
        return self._response

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """
        :return:
        """
        return self._soup

    @property
    def tables(self) -> dict[str, pd.DataFrame]:
        """
        :return:
        """
        return self._tables

    def _scrape_tables(self) -> dict[str, pd.DataFrame]:
        """
        :return:
        """
        res = {}

        for name, css in self._css.items():
            elem = self.soup.select_one(css)

            if elem is None:
                df_ = None
            else:
                try:
                    df_ = pd.read_html(str(elem))[0]
                except ValueError:
                    df_ = pd.read_html(
                        elem.find(
                            string=lambda s: isinstance(s, bs4.Comment)
                        )
                    )[0]

            res.setdefault(name, df_)

        return res

    def standard_batting(self, minors: bool = False) -> _StandardBatting:
        """
        :return:
        """
        df_ = self.tables.get("Standard Batting")

        if not minors:
            df_.drop(
                index=[
                    s for s in df_.index
                    if isinstance(df_.loc[s, "Tm"], str) and "min" in df_.loc[s, "Tm"]
                ],
                inplace=True
            )
            df_.reset_index(drop=True, inplace=True)

        dividers = [s for s in df_.index if df_.loc[s].isna().all()]
        if len(dividers) == 2:
            seasons, career, season_average, teams, leagues = (
                df_.iloc[:dividers[0] - 2, :].copy(),
                df_.iloc[(dividers[0] - 2), :].copy(),
                df_.iloc[(dividers[0] - 1), :].copy(),
                df_.iloc[(dividers[0] + 1):dividers[1], :].copy(),
                df_.iloc[(dividers[1] + 1):, :].copy()
            )
        elif len(dividers) == 1:
            seasons, career, season_average, teams, leagues = (
                df_.iloc[:dividers[0] - 2, :].copy(),
                df_.iloc[(dividers[0] - 2), :].copy(),
                df_.iloc[(dividers[0] - 1), :].copy(),
                df_.iloc[(dividers[0] + 1):, :].copy(),
                None
            )
        else:
            seasons, career, season_average, teams, leagues = (
                df_.iloc[:-2, :].copy(),
                df_.iloc[-2, :].copy(),
                df_.iloc[-1, :].copy(),
                None,
                None
            )

        seasons.loc[:, "Lg"] = seasons.loc[:, "Lg"].apply(
            lambda x: x.split(",")
        )
        seasons.loc[:, "Pos"] = seasons.loc[:, "Pos"].apply(
            lambda x: re.findall(r"[*/][0-9HD]", x) if isinstance(x, str) else np.nan
        )
        seasons.loc[:, "Awards"] = seasons.loc[:, "Awards"].apply(
            lambda x: (np.nan if "\xa0" in x else x.split(",")) if isinstance(x, str) else np.nan
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
                "Tm": [re.search(r"[A-Z]+", x).group() for x in teams.iloc[:, 0]],
                "Yrs": [int(re.search(r"\d+", x).group()) for x in teams.iloc[:, 0]]
            }
            teams = pd.concat(
                [
                    pd.DataFrame(_add),
                    teams.reset_index(drop=True).iloc[:, 4:]
                ], axis=1
            )

        if leagues is not None:
            leagues.drop(columns=["Pos", "Awards"], inplace=True)
            _add = {
                "Lg": [re.search(r"[A-Z]+", x).group() for x in leagues.iloc[:, 0]],
                "Yrs": [int(re.search(r"\d+", x).group()) for x in leagues.iloc[:, 0]]
            }
            leagues = pd.concat(
                [
                    pd.DataFrame(_add),
                    leagues.reset_index(drop=True).iloc[:, 4:]
                ], axis=1
            )

        return self._StandardBatting(seasons, career, season_average, teams, leagues)

    def player_value(self) -> _PlayerValue:
        """
        :return:
        """
        df_ = self.tables.get("Player Value")

        dividers = [s for s in df_.index if df_.loc[s].isna().all()]
        if dividers:
            seasons, career, season_average, teams = (
                df_.iloc[:(dividers[0] - 2)].copy(),
                df_.iloc[dividers[0] - 2].copy(),
                df_.iloc[dividers[0] - 1].copy(),
                df_.iloc[(dividers[0] + 1):].copy()
            )
        else:
            seasons, career, season_average, teams = (
                df_.iloc[:-2].copy(),
                df_.iloc[-2].copy(),
                df_.iloc[-1].copy(),
                None
            )

        seasons.loc[:, "Pos"] = seasons.loc[:, "Pos"].apply(
            lambda x: re.findall(r"[*/][0-9HD]", x) if isinstance(x, str) else np.nan
        )
        seasons.loc[:, "Awards"] = seasons.loc[:, "Awards"].apply(
            lambda x: (np.nan if "\xa0" in x else x.split(",")) if isinstance(x, str) else np.nan
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
                "Tm": [re.search(r"[A-Z]+", x).group() for x in teams.iloc[:, 0]],
                "Yrs": [int(re.search(r"\d+", x).group()) for x in teams.iloc[:, 0]]
            }
            teams = pd.concat(
                [
                    pd.DataFrame(_add),
                    teams.reset_index(drop=True).iloc[:, 4:]
                ], axis=1
            )

        return self._PlayerValue(seasons, career, season_average, teams)

    def advanced_batting(self) -> _AdvancedBatting:
        """
        :return:
        """
        df_ = self.tables.get("Advanced Batting")
        df_.columns = df_.columns.droplevel()

        seasons, career, mlb_averages = (
            df_.iloc[:-2], df_.iloc[-2], df_.iloc[-1]
        )

        _add = {
            "Yrs": int(re.search(r"\d+", career.iloc[0]).group())
        }
        career = pd.concat([pd.Series(_add), career.iloc[4:]])

        mlb_averages = mlb_averages.iloc[4:]

        return self._AdvancedBatting(seasons, career, mlb_averages)

    def postseason_batting(self) -> typing.Optional[_PostseasonBatting]:
        """
        :return:
        """
        seasons_regex = re.compile(r"^\d+$")
        career_regex = re.compile(r"^(\d+) Yrs \((\d+) Series\)$")
        series_types_regex = re.compile(r"^(\d+) (WS|((AL|NL)(WC|DS|CS)))$")

        df_ = self.tables.get("Postseason Batting")
        if df_ is None:
            return
        df_.dropna(how="all", inplace=True)
        df_ = df_.reset_index(drop=True)

        seasons = df_.iloc[
            [x for x in df_.index if seasons_regex.search(str(df_.loc[x, "Year"]))]
        ]
        try:
            career = df_.iloc[
                [x for x in df_.index if career_regex.search(str(df_.loc[x, "Year"]))][0]
            ]
        except IndexError:
            career = None
        series_types = df_.iloc[
            [x for x in df_.index if series_types_regex.search(str(df_.loc[x, "Year"]))]
        ]

        if career is not None:
            _add = {
                "Yrs": int(career_regex.search(career.iloc[0]).group(1)),
                "Series": int(career_regex.search(career.iloc[0]).group(2))
            }
            career = pd.concat([pd.Series(_add), career.iloc[7:]])

        if series_types is not None:
            _add = {
                "Type": [series_types_regex.search(x).group(2) for x in series_types.iloc[:, 0]],
                "Count": [series_types_regex.search(x).group(1) for x in series_types.iloc[:, 0]]
            }
            series_types = pd.concat(
                [
                    pd.DataFrame(_add),
                    series_types.reset_index(drop=True).iloc[:, 7:]
                ], axis=1
            )

        return self._PostseasonBatting(seasons, career, series_types)

    def standard_fielding(self) -> _StandardFielding:
        """
        :return:
        """
        seasons_regex = re.compile(r"^\d+$")
        positions_regex = re.compile(r"^(\d+) Seasons?$")

        df_ = self.tables.get("Standard Fielding")

        seasons = df_.iloc[
            [x for x in df_.index if seasons_regex.search(str(df_.iloc[x, 0]))]
        ].copy()
        positions = df_.iloc[
            [x for x in df_.index if positions_regex.search(str(df_.iloc[x, 0]))]
        ].copy()

        seasons.loc[:, "Awards"] = seasons.loc[:, "Awards"].apply(
            lambda x: (np.nan if "\xa0" in x else x.split(",")) if isinstance(x, str) else np.nan
        )

        positions.drop(columns=["Lg", "Awards"], inplace=True)
        _add = {
            "Seasons": [int(positions_regex.search(x).group(1)) for x in positions.iloc[:, 0]]
        }
        positions = pd.concat(
            [
                positions.reset_index(drop=True).iloc[:, 3],
                pd.DataFrame(_add),
                positions.reset_index(drop=True).iloc[:, 5:]
            ], axis=1
        )

        return self._StandardFielding(seasons, positions)

    def appearances(self) -> _Appearances:
        """
        :return:
        """
        seasons_regex = re.compile(r"^(\d+) Seasons$")

        df_ = self.tables.get("Appearances")

        seasons = df_.iloc[:-1, :].copy()
        total = df_.iloc[-1].copy()

        total.drop(columns=["Lg"], inplace=True)
        _add = {
            "Seasons": int(seasons_regex.search(total.iloc[0]).group(1))
        }
        total = pd.concat([pd.Series(_add), total.iloc[4:]])

        return self._Appearances(seasons, total)

    def leaderboard(self) -> dict[str, pd.Series]:
        """
        :return:
        """
        container = self.soup.select_one(
            self._css.get("Leaderboard")
        ).find(string=lambda s: isinstance(s, bs4.Comment))
        soup_ = bs4.BeautifulSoup(container, features="lxml")

        titles = [x.text for x in soup_.select("table > caption")]
        dfs = pd.read_html(container)

        return dict(zip(titles, [pd.Series(x.iloc[:, 0]) for x in dfs]))

    def hall_of_fame_statistics(self):
        """
        :return:
        """
        pass

    def salaries(self) -> typing.Optional[_Salaries]:
        """
        :return:
        """
        df_ = self.tables.get("Salaries")
        if df_ is None:
            return
        df_.dropna(how="all", inplace=True)
        df_.reset_index(drop=True)

        _all = re.findall(r"\d+", df_.iloc[-2, 2])
        if len(_all) == 2:
            arbitration_eligible = int(_all[0])
            free_agent = int(_all[1])
        else:
            arbitration_eligible = None
            free_agent = int(_all[0])

        career_to_date = int("".join(re.findall(r"\d+", df_.iloc[-1, 3])))

        df_.drop(index=df_.index[-2:], inplace=True)

        return self._Salaries(df_, arbitration_eligible, free_agent, career_to_date)
