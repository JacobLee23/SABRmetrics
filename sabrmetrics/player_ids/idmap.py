"""

"""

import datetime
import json
import math
import os
import typing

import pandas as pd
import requests
import numpy as np

from ._sfbb import HEADERS
from ._sfbb import SFBBTools


class _DFReformat:
    """

    """
    class ColumnsReformat(typing.NamedTuple):
        """

        """
        columns: typing.Tuple[str]
        col_map: typing.Dict[str, str]

    class IDMapReformat(ColumnsReformat):
        """

        """
        _directory = os.path.join("sabrmetrics", "player_ids", "data", "columns")
        columns_path = os.path.join(_directory, "idmap_columns.json")
        colmap_path = os.path.join(_directory, "idmap_colmap.json")
        paths = (columns_path, colmap_path)

        @staticmethod
        def reformat_birthdate(birthdate: str) -> datetime.datetime:
            """

            """
            if not isinstance(birthdate, str):
                if isinstance(birthdate, float) and math.isnan(birthdate):
                    return np.nan
                raise TypeError
            try:
                return datetime.datetime.strptime(birthdate, "%m/%d/%Y")
            except ValueError:
                return datetime.datetime.strptime(birthdate, "%m/%d/%y")

        @staticmethod
        def reformat_all_positions(all_positions: str) -> list[str]:
            """

            """
            if not isinstance(all_positions, str):
                if isinstance(all_positions, float) and math.isnan(all_positions):
                    return np.nan
                raise TypeError
            return all_positions.split("/")

        @staticmethod
        def reformat_active(active: str) -> bool:
            """

            """
            if not isinstance(active, str):
                if isinstance(active, float) and math.isnan(active):
                    return np.nan
                raise TypeError
            active = active.upper()
            if active == "Y":
                return True
            if active == "N":
                return False
            raise ValueError

    class ChangeLogReformat:
        """

        """
        _directory = os.path.join("sabrmetrics", "player_ids", "data", "columns")
        columns_path = os.path.join(_directory, "changelog_columns.json")
        colmap_path = os.path.join(_directory, "changelog_colmap.json")
        paths = (columns_path, colmap_path)

    @classmethod
    def load_reformat(cls, columns_path: str, colmap_path: str) -> ColumnsReformat:
        """

        """
        with open(columns_path, "r", encoding="utf-8") as file:
            columns = json.load(file)
        with open(colmap_path, "r", encoding="utf-8") as file:
            column_map = json.load(file)

        reformat = cls.ColumnsReformat(columns=columns, col_map=column_map)
        return reformat


class IDMap:
    """

    """
    _integer_columns = [
        "BaseballHQID", "BaseballProspectusID", "CBSID", "ESPNID", "FanDuelID",
        "MLBID", "NFBCID", "OttoneuID", "RotoWireID", "YahooID"
    ]

    def __init__(self):
        self._sfbb = SFBBTools()

    class _DFReformat(typing.NamedTuple):
        """

        """
        columns: typing.Tuple[str]
        col_map: typing.Dict[str, str]

    @property
    def excel_download(self) -> str:
        """

        """
        return self._sfbb.urls.excel_download

    @property
    def web_view(self) -> str:
        """

        """
        return self._sfbb.urls.web_view

    @property
    def csv_download(self) -> str:
        """

        """
        return self._sfbb.urls.csv_download

    @property
    def changelog_web_view(self) -> str:
        """

        """
        return self._sfbb.urls.changelog_web_view

    @property
    def changelog_csv_download(self) -> str:
        """

        """
        return self._sfbb.urls.changelog_csv_download

    def save_excel(self, path: str) -> str:
        """

        """
        res = requests.get(self.excel_download, headers=HEADERS)

        with open(path, "wb") as file:
            file.write(res.content)

        return os.path.abspath(path)

    def save_csv(self, path: str) -> str:
        """

        """
        res = requests.get(self.csv_download, headers=HEADERS)

        with open(path, "wb") as file:
            file.write(res.content)

        return os.path.abspath(path)

    def save_changelog_csv(self, path: str) -> str:
        """

        """
        res = requests.get(self.changelog_csv_download, headers=HEADERS)

        with open(path, "wb") as file:
            file.write(res.content)

        return os.path.abspath(path)

    def read_data(self) -> pd.DataFrame:
        """

        """
        res = requests.get(self.web_view, headers=HEADERS)
        df_ = pd.read_html(res.text)[0]

        df_.rename(columns=df_.iloc[0], inplace=True)
        df_.drop(
            index=[df_.index[0], df_.index[1]],
            columns=[df_.columns[0]],
            inplace=True
        )
        df_.dropna(axis=1, how="all", inplace=True)

        df_ = self._format_idmap_df(df_)

        return df_

    def _format_idmap_df(self, df_: pd.DataFrame) -> pd.DataFrame:
        """

        """
        reformat = _DFReformat.load_reformat(*_DFReformat.IDMapReformat.paths)

        df_.rename(
            index=lambda i: i - df_.index[0],
            columns=reformat.col_map,
            inplace=True
        )
        df_ = df_.reindex(columns=reformat.columns)
        df_.loc[:, "Birthdate"] = df_.loc[:, "Birthdate"].apply(
            _DFReformat.IDMapReformat.reformat_birthdate
        )
        df_.loc[:, "AllPositions"] = df_.loc[:, "AllPositions"].apply(
            _DFReformat.IDMapReformat.reformat_all_positions
        )
        df_.loc[:, "Active"] = df_.loc[:, "Active"].apply(
            _DFReformat.IDMapReformat.reformat_active
        )
        df_.loc[:, self._integer_columns] = df_.loc[:, self._integer_columns].applymap(
            lambda x: 0 if math.isnan(float(x)) else int(x)
        )

        return df_

    def read_changelog(self) -> pd.DataFrame:
        """

        """
        res = requests.get(self.changelog_web_view, headers=HEADERS)
        df_ = pd.read_html(res.text)[0]

        df_.rename(columns=df_.iloc[0], inplace=True)
        df_.drop(index=df_.index[0], inplace=True)

        df_ = self._format_changelog_df(df_)

        return df_

    def _format_changelog_df(self, df_: pd.DataFrame) -> pd.DataFrame:
        """

        """
        reformat = _DFReformat.load_reformat(*_DFReformat.ChangeLogReformat.paths)

        df_.rename(
            index=lambda i: i - df_.index[0],
            columns=reformat.col_map,
            inplace=True
        )
        df_ = df_.reindex(columns=reformat.columns)
        df_.loc[:, "Date"] = df_.loc[:, "Date"].apply(
            lambda x: datetime.datetime.strptime(x, "%m/%d/%Y")
        )

        return df_
