"""
Wrapper for the various Player ID databases in the codebase.

- `Smart Fantasy Baseball`_: :py:class:`sabrmetrics.sfbb.tools.PlayerIDMap`

.. _Smart Fantasy Baseball: https://smartfantasybaseball.com/
"""

import pandas as pd

from sabrmetrics import sfbb


class _SmartFantasyBaseball:
    """
    Wrapper for :py:class:`sabrmetrics.sfbb.tools.PlayerIDMap`.
    """
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
        self._pidmap: pd.DataFrame = self._obj.playeridmap

    def __getitem__(self, item: str) -> pd.DataFrame:
        """

        :param item:
        :return:
        """
        columns: list[str] = self._site_columns[item]

        return self.pidmap.loc[:, columns]

    @property
    def pidmap(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._pidmap

    @property
    def sites(self) -> tuple[str]:
        """

        :return:
        """
        return tuple(self._site_columns.keys())
