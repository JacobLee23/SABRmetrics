"""

"""

import dataclasses
import datetime
import typing

import requests

from . import league
from .address import Address_
from .league import AmericanLeague, NationalLeague
from .scraper import APIScraper
from sabrmetrics import TODAY


class Address(Address_):
    """
    """
    base = "https://statsapi.mlb.com/api/v1/standings"

    class _FieldDefaults(typing.NamedTuple):
        """
        """
        league_id: typing.Tuple[int] = (
            AmericanLeague().fields["league_id"], NationalLeague().fields["league_id"]
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

    def concatenate(self) -> str:
        queries = {}
        if self["league_id"]:
            queries.setdefault("leagueId", ",".join(map(str, self["league_id"])))
        if self["season"]:
            queries.setdefault("season", str(self["season"]))
        if self["date"]:
            queries.setdefault("date", self["date"].strftime("%Y-%m-%d"))
        if self["standings_types"]:
            queries.setdefault("standingsTypes", ",".join(self["standings_types"]))
        if self["hydrate"]:
            queries.setdefault("hydrate", ",".join(self["hydrate"]))

        return f"{self.base}?{'&'.join(f'{k}={v}' for k, v in queries.items())}"


class Standings(APIScraper):
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
        kwargs = {}
        if league_id:
            kwargs.setdefault("league_id", tuple(map(int, league_id)))
        if season:
            kwargs.setdefault("season", int(season))
        if date:
            szn = league.Season(date.year)
            if not (szn["regularSeasonStartDate"] <= date <= szn["regularSeasonEndDate"]):
                date = league.Season.latest(date)["regularSeasonEndDate"]
            kwargs.setdefault("date", date)

        super().__init__(Address(**kwargs))
