"""

"""

import datetime
import typing

import pandas as pd

from . import divisions
from . import leagues
from .address import APIAddress
from .divisions import Division
from .leagues import League
from .leagues import Season
from .scraper import APIScraper


LEAGUES = [
    leagues.AmericanLeague, leagues.NationalLeague
]
DIVISIONS = [
    divisions.ALWest, divisions.ALEast, divisions.ALCentral,
    divisions.NLWest, divisions.NLEast, divisions.NLCentral
]


class Address(APIAddress):
    """
    """
    url = "https://statsapi.mlb.com/api/v1/standings"
    field_defaults = {
        "league_id": (leagues.AmericanLeague.league_id, leagues.NationalLeague.league_id),
        "season": Season.latest_year(),
        "date": Season.latest_date(),
        "standings_types": ("regularSeason", "springTraining", "firstHalf", "secondHalf"),
        "hydrate": (
            "division", "conference", "sport", "league",
            "team({next_schedule},{previous_schedule})".format(
                next_schedule="nextSchedule(team,gameType=[R,F,D,L,W,C],inclusive=false)",
                previous_schedule="previousSchedule(team,gameType=[R,F,D,L,W,C],inclusive=true)"
            )
        )
    }

    @property
    def parameters(self) -> typing.Dict[str, str]:
        """
        """
        return {
            "leagueId": self.league_id, "season": self.season, "date": self.date,
            "standingsTypes": self.standings_types
        }

    @property
    def league_id(self) -> str:
        """
        """
        return ",".join(map(str, self.fields["league_id"]))
    
    @property
    def season(self) -> str:
        """
        """
        return str(self.fields["season"])
    
    @property
    def date(self) -> str:
        """
        """
        return self.fields["date"].strftime("%Y-%m-%d")
    
    @property
    def standings_types(self) -> str:
        """
        """
        return ",".join(self.fields["standings_types"])
    
    @property
    def hydrate(self) -> str:
        """
        """
        return ",".join(self.fields["hydrate"])


class Standings(APIScraper):
    """
    :param view:
    :param league_id:
    :param season:
    :param date:
    """
    def __init__(
        self, *, view: typing.Union[typing.Type[Division], typing.Type[League]] = None,
        league_id: typing.Optional[typing.Sequence[int]] = None,
        season: typing.Optional[int] = None,
        date: typing.Optional[datetime.datetime] = None
    ):
        address = Address(
            league_id=tuple(map(int, league_id)) if league_id else None,
            season=int(season) if season else None,
            date=Season.latest_date(date) if date else None
        )
        super().__init__(address)

        if view is None or not isinstance(view, type):
            self._records = self.data["records"]
        elif issubclass(view, League):
            self._records = filter(
                lambda x: x["league"]["id"] == view.league_id, self.data["records"]
            )
        elif issubclass(view, Division):
            self._records = filter(
                lambda x: x["division"]["id"] == view.division_id, self.data["records"]
            )

        self._dataframe = pd.concat(pd.DataFrame(x["teamRecords"]) for x in self._records)
        self._dataframe.reset_index(drop=True, inplace=True)

    @property
    def team(self) -> pd.DataFrame:
        """
        """
        return pd.DataFrame(list(self._dataframe.loc[:, "team"]))

    @property
    def streak(self) -> pd.DataFrame:
        """
        """
        return pd.DataFrame(list(self._dataframe.loc[:, "streak"]))
    
    @property
    def league_record(self) -> pd.DataFrame:
        """
        """
        return pd.DataFrame(list(self._dataframe.loc[:, "leagueRecord"]))

    def standings(self) -> pd.DataFrame:  
        """
        :return:
        """
        return pd.concat(
            [
                self.team, self._dataframe.loc[:, "season"], self.streak,
                self._dataframe.loc[:, "divisionRank":"leagueRecord"], self.league_record,
                self._dataframe.loc[:, "runsAllowed":]
            ], axis=1
        )