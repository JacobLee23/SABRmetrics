"""
"""

import datetime
import typing

import requests

from .address import APIAddress
from .scraper import APIScraper
from sabrmetrics import TODAY


class Address(APIAddress):
    """
    """
    url = "https://statsapi.mlb.com/api/v1/league/{league_id}"
    field_defaults = {"season": TODAY.year}

    @property
    def season(self) -> str:
        """
        """
        return str(self.fields["season"])


class League(APIScraper):
    """
    :param league_id:
    :param season:
    """
    def __init__(self, league_id: int, season: int):
        kwargs = {}
        kwargs.setdefault("league_id", int(league_id))
        kwargs.setdefault("season", int(season))
        
        super().__init__(Address(**kwargs))

    @classmethod
    def all_data(cls, season: int) -> dict:
        """
        :param season:
        """
        address = Address(season=season)
        url = address.concatenate()

        with requests.get(url) as response:
            return response.json()


class AmericanLeague(League):
    """
    :param season:
    """
    url = Address.url.format(league_id=103)

    def __init__(self, season: int = TODAY.year):
        super().__init__(season)


class NationalLeague(League):
    """
    :param season:
    """
    url = Address.url.format(league_id=104)

    def __init__(self, season: int = TODAY.year):
        super().__init__(season)


class CactusLeague(League):
    """
    :param season:
    """
    url = Address.url.format(league_id=114)

    def __init__(self, season: int = TODAY.year):
        super().__init__(season)


class GrapefruitLeague(League):
    """
    :param season:
    """
    url = Address.url.format(league_id=115)

    def __init__(self, season: int = TODAY.year):
        super().__init__(season)


class Season:
    """
    :param year:
    :param league:
    """
    date_spans = {
        "preseaon": ("preSeasonStartDate", "preSeasonEndDate"),
        "season": ("seasonStartDate", "seasonEndDate"),
        "spring": ("springStartDate", "springEndDate"),
        "regular-season": ("regularSeasonStartDate", "regularSeasonEndDate"),
        "first-half": ("regularSeasonStartDate", "lastDate1stHalf"),
        "second-half": ("firstDate2ndHalf", "regularSeasonEndDate"),
        "postseason": ("postSeasonStartDate", "postSeasonEndDate"),
        "offseason": ("offSeasonStartDate", "offSeasonEndDate")
    }

    def __init__(self, year: int = TODAY.year, *, league: League = AmericanLeague):
        self._year = year
        self._data = league(year)["leagues"][0]["seasonDateInfo"]

    def __getitem__(self, key: str) -> typing.Union[int, float, str, datetime.datetime]:
        value = self.data[key]

        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                try:
                    return datetime.datetime.strptime(value, "%Y-%m-%d")
                except ValueError:
                    return str(value)

    @classmethod
    def latest_season(
        cls, date: datetime.datetime = TODAY, span: str = "regular-season"
    ) -> "Season":
        """
        :param date:
        :param span:
        :return:
        :raise ValueError:
        """
        season = cls(date.year)
        keys = cls.date_spans[span]
        start = season[keys[0]]

        if datetime.datetime(date.year, 1, 1) <= date < start:
            return cls(date.year - 1)
        elif start <= date <= datetime.datetime(date.year, 12, 31):
            return season
        else:
            raise ValueError(date)

    @classmethod
    def latest_year(cls, date: datetime.datetime = TODAY, span: str = "regular-season") -> int:
        """
        :param date:
        :param span:
        :return:
        """
        return cls.latest_season(date, span).year

    @classmethod
    def latest_date(cls, date: datetime.datetime = TODAY, span: str = "regular-season") -> int:
        """
        :param date:
        :return:
        :raise ValueError:
        """
        season = cls(date.year)
        keys = cls.date_spans[span]
        start, end = season[keys[0]], season[keys[1]]

        if start <= date <= end:
            return date
        return cls.latest_season(date, span)[keys[1]]

    @property
    def data(self) -> dict:
        """
        :return:
        """
        return self._data

    @property
    def year(self) -> int:
        """
        :return:
        """
        return self._year

    def date_range(
        self, span: str = "regular-season"
    ) -> typing.Tuple[datetime.datetime, datetime.datetime]:
        """
        :param span:
        :return:
        """
        keys = self.date_spans[span]
        return self[keys[0]], self[keys[1]]

    def date_in_span(
        self, date: datetime.datetime = TODAY, span: str = "regular-season"
    ) -> bool:
        """
        :param date:
        :param span:
        :return:
        """
        start, end = self.date_range(span)
        return start <= date <= end
