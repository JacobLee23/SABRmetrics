"""
Wrapper for the various Player ID databases in the codebase.

- `Smart Fantasy Baseball`_: :py:class:`sabrmetrics.sfbb.tools.PlayerIDMap`

.. _Smart Fantasy Baseball: https://smartfantasybaseball.com/
"""

import typing

import pandas as pd

from sabrmetrics import sfbb


class _Flavor:
    """

    """
    def __init__(
            self, name: str, pidmap: pd.DataFrame,
            *, primary_columns: list[str], site_columns: dict[str, list[str]]
    ):
        """

        :param name:
        :param pidmap:
        :param primary_columns:
        :param site_columns:
        """
        self._name = name
        self._pidmap = pidmap

        self._primary_columns = primary_columns
        self._site_columns = site_columns

    def __repr__(self) -> str:
        """

        :return:
        """
        return f"_Flavor(name='{self.name}')"

    @property
    def name(self) -> str:
        """

        :return:
        """
        return self._name

    @property
    def pidmap(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._pidmap

    @property
    def primary_columns(self) -> list[str]:
        """

        :return:
        """
        return self._primary_columns

    @property
    def site_columns(self) -> dict[str, list[str]]:
        """

        :return:
        """
        return self._site_columns


class _SmartFantasyBaseball(_Flavor):
    """
    Wrapper for :py:class:`sabrmetrics.sfbb.tools.PlayerIDMap`.
    """
    __name = "SmartFantasyBaseball"

    __primary_columns: list[str] = [
        "PlayerID", "Name", "LastName", "FirstName", "LastFirst",
        "Birthdate", "Team", "League", "Position", "AllPositions",
        "Bats", "Throws", "Active"
    ]
    __site_columns: dict[str, list[str]] = {
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

        super().__init__(
            self.__name, self._obj.playeridmap,
            primary_columns=self.__primary_columns,
            site_columns=self.__site_columns
        )


class PlayerIDs:
    """

    """
    __flavors = {
        "SmartFantasyBaseball": _SmartFantasyBaseball
    }

    def __init__(self, flavor: typing.Union[str, _Flavor]):
        """

        :param flavor:
        """
        if isinstance(flavor, str):
            self._flavor = self.get_flavor(flavor)
        elif isinstance(flavor, _Flavor):
            self._flavor = flavor
        else:
            raise TypeError(
                f"Expected str or _Flavor, got {type(flavor)}"
            )

    def __getitem__(self, item: str):
        """

        :param item:
        :return:
        """
        return pd.concat(
            [self.primary_df, self.site_df(item)],
            axis=1
        )

    @classmethod
    def get_flavor(cls, name: str) -> _Flavor:
        """

        :param name:
        :return:
        """
        flavor_cls = cls.__flavors[name]
        flavor = flavor_cls()

        return flavor

    @property
    def pidmap(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._flavor.pidmap

    @property
    def sites(self) -> tuple[str]:
        """

        :return:
        """
        return tuple(self._flavor.site_columns)

    @property
    def primary_df(self) -> pd.DataFrame:
        """

        :return:
        """
        return self.pidmap.loc[:, self._flavor.primary_columns]

    def site_df(self, name: str) -> pd.DataFrame:
        """

        :param name:
        :return:
        """
        columns = self._flavor.site_columns[name]

        return self.pidmap.loc[:, columns]
