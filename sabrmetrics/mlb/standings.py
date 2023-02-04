"""

"""

import dataclasses
import datetime
import typing

import requests

from . import league
from .address import Address_
from .league import AmericanLeague, NationalLeague
from sabrmetrics import TODAY


class Address(Address_):
    base = "https://statsapi.mlb.com/api/v1/standings"

    @dataclasses.dataclass
    class Fields:
        """
        :param league_id:
        :param season:
        :param date:
        :param standings_types:
        :param hydrate:
        """
        league_id: typing.Tuple[int] = tuple(
            lg().data["leagues"][0]["id"] for lg in [
                AmericanLeague, NationalLeague
            ]
        )
        season: int = league.Season.latest().year
        date: datetime.datetime = min(TODAY, league.Season.latest()["regularSeasonEndDate"])
        standings_types: typing.Tuple[str] = (
            "regularSeason", "springTraining", "firstHalf", "secondHalf"
        )
        hydrate: typing.Tuple[str] = (
            "division", "conference", "sport", "league",
            "team({next_schedule},{previous_schedule})".format(
                next_schedule="nextSchedule(team,gameType=[R,F,D,L,W,C],inclusive=false)",
                previous_schedule="previousSchedule(team,gameType=[R,F,D,L,W,C],inclusive=true)"
            )
        )

    @classmethod
    def concatenate(cls, fields: Fields) -> str:
        cls.check_address_fields(fields)

        queries = {}
        if fields.league_id:
            queries.setdefault("leagueId", ",".join(map(str, fields.league_id)))
        if fields.season:
            queries.setdefault("season", str(fields.season))
        if fields.date:
            queries.setdefault("date", fields.date.strftime("%Y-%m-%d"))
        if fields.standings_types:
            queries.setdefault("standingsTypes", ",".join(fields.standings_types))
        if fields.hydrate:
            queries.setdefault("hydrate", ",".join(fields.hydrate))

        address = cls.base + "?" + "&".join(f"{k}={v}" for k, v in queries.items())

        return address


class Standings:
    """
    :param league_id:
    :param season:
    :param date:
    """
    def __init__(
            self, *,
            league_id: typing.Optional[typing.Sequence[int]] = None,
            season: typing.Optional[int] = None,
            date: typing.Optional[datetime.datetime] = None
    ):
        self._fields = Address.defaults()

        if league_id:
            self._fields.league_id = tuple(map(int, league_id))
        if season:
            self._fields.season = int(season)
        if date:
            szn = league.Season(date.year)
            if not (szn["regularSeasonStartDate"] <= date <= szn["regularSeasonEndDate"]):
                date = league.Season.latest(date)["regularSeasonEndDate"]
            self._fields.date = date

        self._address = Address.concatenate(self.fields)

        self._response = requests.get(self.address)
        self._data = self.response.json()

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

    @property
    def data(self) -> dict:
        """

        :return:
        """
        return self._data

    @property
    def fields(self) -> Address.Fields:
        """
        :return:
        """
        return self._fields
