"""

"""

import datetime
import typing

import numpy as np
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
        self._dataframe.replace("-", np.nan, inplace=True)

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

    @property
    def split_records(self) -> pd.DataFrame:
        """
        """
        return self._flat_record(
            list(self._dataframe.loc[:, "records"]), "splitRecords"
        )

    @property
    def division_records(self) -> pd.DataFrame:
        """
        """
        return self._nested_record(
            list(self._dataframe.loc[:, "records"]), "divisionRecords", "division"
        )
    
    @property
    def overall_records(self) -> pd.DataFrame:
        """
        """
        return self._flat_record(
            list(self._dataframe.loc[:, "records"]), "overallRecords"
        )
    
    @property
    def league_records(self) -> pd.DataFrame:
        """
        """
        return self._nested_record(
            list(self._dataframe.loc[:, "records"]), "leagueRecords", "league"
        )

    @property
    def expected_records(self) -> pd.DataFrame:
        """
        """
        return self._flat_record(
            list(self._dataframe.loc[:, "records"]), "expectedRecords"
        )

    def standings(
        self, *,
        advanced: typing.Literal["split", "division", "overall", "league", "expected"] = None,
        streak: bool = True,
        league_record: bool = True
    ) -> pd.DataFrame:  
        """
        :param advanced:
        :param streak:
        :param league_record:
        :return:
        """
        df_standard = pd.concat(
            [self._dataframe.drop(columns=["team", "streak", "leagueRecord", "records"])],
            keys=["standard"], axis=1
        )
        df_team = pd.concat([self.team], keys=["team"], axis=1)

        dataframe = pd.concat([df_team, df_standard], axis=1)
            
        if advanced == "split":
            dataframe = dataframe.join(self.split_records)
        elif advanced == "division":
            dataframe = dataframe.join(self.division_records)
        elif advanced == "overall":
            dataframe = dataframe.join(self.overall_records)
        elif advanced == "league":
            dataframe = dataframe.join(self.league_records)
        elif advanced == "expected":
            dataframe = dataframe.join(self.expected_records)
        
        if streak:
            dataframe = dataframe.join(
                pd.concat([self.streak], keys=["streak"], axis=1)
            )
        if league_record:
            dataframe = dataframe.join(
                pd.concat([self.league_record], keys=["leagueRecord"], axis=1)
            )

        return dataframe

    def _flat_record(
        self, records: typing.List[typing.Dict], key: str
    ) -> pd.DataFrame:
        """
        :param records:
        :param key:
        :return:
        """
        series = []

        for record in records:
            dataframe = pd.DataFrame(record[key])

            dataframe.rename(index=dataframe.loc[:, "type"], inplace=True)
            dataframe.drop(columns=["type"], inplace=True)

            series.append(dataframe.stack())

        return pd.DataFrame(series)
    
    def _nested_record(
        self, records: typing.List[typing.Dict], key: str, inner_key: str
    ) -> pd.DataFrame:
        """
        :param records:
        :param key:
        :param inner_key:
        :return:
        """
        series = []

        for record in records:
            dataframe = pd.DataFrame(record[key])

            nested_df = pd.DataFrame(list(dataframe.loc[:, inner_key]))
            nested_df.columns = pd.MultiIndex.from_product([[inner_key], nested_df.columns])

            series.append(pd.concat([dataframe.iloc[:, :-1], nested_df], axis=1).stack())

        return pd.DataFrame(series)
