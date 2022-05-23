"""

"""

import datetime
import json
import os

import pandas as pd

from . import idmap


class IDMap:
    """

    """
    _sites_path = os.path.join(
        "sabrmetrics", "player_ids", "data", "sites.json"
    )
    with open(_sites_path, "r", encoding="utf-8") as file:
        _sites = json.load(file)

    def __init__(self):
        self._idmap = idmap.IDMap()
        self._data = self.idmap.read_data()
        self._changelog = self.idmap.read_changelog()

        self.__info = [
            "LastName", "FirstName", "PlayerName", "LastFirstName", "Birthdate", "PlayerID"
        ]
        self.__general = [
            "Bats", "Throws", "Team", "League", "Position", "AllPositions", "Active"
        ]

    def __getitem__(self, item: str) -> pd.DataFrame:
        """

        """
        columns = self._sites[item]
        return self.general.join(self.data.loc[:, columns])

    @property
    def idmap(self) -> idmap.IDMap:
        """

        """
        return self._idmap

    @property
    def data(self) -> pd.DataFrame:
        """

        """
        return self._data

    @property
    def changelog(self) -> pd.DataFrame:
        """

        """
        return self._changelog

    @property
    def info(self) -> pd.DataFrame:
        """

        """
        return self.data.loc[:, self.__info]

    @property
    def general(self) -> pd.DataFrame:
        """

        """
        return self.info.join(self.data.loc[:, self.__general])

    @property
    def last_update(self) -> datetime.datetime:
        """

        """
        return self.changelog.loc[0, "Date"]

    @property
    def sites(self) -> list[str]:
        """

        """
        return list(self._sites)
