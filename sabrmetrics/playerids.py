"""
Wrapper for the various Player ID databases in the codebase.

- `Smart Fantasy Baseball`_: :py:class:`sabrmetrics.sfbb.tools.PlayerIDMap`

.. _Smart Fantasy Baseball: https://smartfantasybaseball.com/
"""

import pandas as pd

from sabrmetrics import sfbb


class Flavor:
    """

    """
    _name: str

    _primary_columns: list[str]
    _site_columns: dict[str, list[str]]

    def __init__(self, pidmap: pd.DataFrame):
        """

        :param pidmap:
        """
        self._pidmap = pidmap

    def __getitem__(self, item: str):
        """

        :param item:
        :return:
        """
        return pd.concat(
            [self.primary_df, self.site_df(item)],
            axis=1
        )

    @property
    def name(self) -> str:
        """

        :return:
        """
        return self._name

    @property
    def sites(self) -> tuple[str]:
        """

        :return:
        """
        return tuple(self._site_columns.keys())

    @property
    def pidmap(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._pidmap

    @property
    def primary_df(self) -> pd.DataFrame:
        """

        :return:
        """
        return self.pidmap.loc[:, self._primary_columns]

    def site_df(self, name: str) -> pd.DataFrame:
        """

        :param name:
        :return:
        """
        columns = self._site_columns[name]

        return self.pidmap.loc[:, columns]


class _SmartFantasyBaseball(Flavor):
    """
    Wrapper for :py:class:`sabrmetrics.sfbb.tools.PlayerIDMap`.
    """
    _name = "SmartFantasyBaseball"

    _primary_columns: list[str] = [
        "PlayerID", "Name", "LastName", "FirstName", "LastFirst",
        "Birthdate", "Team", "League", "Position", "AllPositions",
        "Bats", "Throws", "Active"
    ]
    _site_columns: dict[str, list[str]] = {
        "BaseballHQ": ["BaseballHQ"],
        "BaseballProspectus": ["BaseballProspectus"],
        "BaseballReference": ["BaseballReference"],
        "CBS": ["CBSID", "CBSName"],
        "ClayDavenport": ["ClayDavenportID"],
        "DraftKings": ["DraftKingsName"],
        "ESPN": ["ESPNID", "ESPN"],
        "FanDuel": ["FanDuelID", "FanDuelName"],
        "FanGraphs": ["FanGraphsID", "FangraphsName"],
        "FantasyPros": ["FantasyProsName"],
        "FanTrax": ["FanTraxID"],
        "KFFL": ["KFFLName"],
        "Masterball": ["MasterballName"],
        "MLB": ["MLBID", "MLBName"],
        "NFBC": ["NFBCID", "NFBCName", "NFBCLastFirst"],
        "Ottoneu": ["OttoneuID"],
        "Razzball": ["RazzballName"],
        "Retrosheet": ["RetrosheetID"],
        "RotoWire": ["RotoWireID", "RotoWireName"],
        "Yahoo": ["YahooID", "YahooName"],
    }

    def __init__(self):
        """

        """
        self._obj = sfbb.tools.PlayerIDMap()

        super().__init__(self._obj.playeridmap)
