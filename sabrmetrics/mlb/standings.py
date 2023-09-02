"""

"""

import datetime
import typing

from .address import APIAddress
from .league import AmericanLeague, NationalLeague
from .league import Season
from .scraper import APIScraper


class Address(APIAddress):
    """
    """
    url = "https://statsapi.mlb.com/api/v1/standings"
    field_defaults = {
        "league_id": (AmericanLeague.league_id, NationalLeague.league_id),
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
    def league_id(self) -> str:
        """
        """
        return ",".join(map(str, self.fields["leagueId"]))
    
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
        address = Address(
            league_id=tuple(map(int, league_id)) if league_id else None,
            season=int(season) if season else None,
            date=Season.latest_date(date) if date else None
        )
        super().__init__(address)
