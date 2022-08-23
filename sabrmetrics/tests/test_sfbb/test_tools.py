"""
Tests for :py:mod:`sabrmetrics.sfbb.tools`.
"""

import datetime
import os
import pathlib

import pandas as pd
import pytest
import requests

from sabrmetrics.sfbb import tools


def test_url():
    """
    Unit test for :py:data:`sabrmetrics.sfbb.tools.URL`.
    """
    with requests.get(tools.URL, headers=tools.HEADERS) as response:
        assert response.status_code == 200


class TestPlayerIDMap:
    """
    Tests for :py:class:`sabrmetrics.sfbb.tools.PlayerIDMap`.
    """
    x = tools.PlayerIDMap()

    def test_headers(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap.headers`.

        Tested in :py:func:`sabrmetrics.tests.test_sfbb.test_headers.test_headers`.
        """
        pytest.skip()

    def test_response(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap.response`.
        """
        assert self.x.response.status_code == 200

    def test_soup(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap.soup`.
        """
        assert self.x.soup
        assert self.x.soup.select_one("html")

    def test_id_maps(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap.id_maps`.
        """
        assert self.x.id_maps
        assert len(self.x.id_maps) == 5
        for url in self.x.id_maps._asdict().values():
            with requests.get(url, headers=self.x.headers) as response:
                assert response.status_code == 200

    def test_playeridmap_table(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap._playeridmap_table`.
        """
        table = self.x._playeridmap_table
        assert table is not None

        dataframes = pd.read_html(str(table))
        assert len(dataframes) == 1

    def test_playeridmap_dataframe(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap._playeridmap_dataframe`.
        """
        df = self.x._playeridmap_dataframe
        assert len(df.columns) == len(self.x._playeridmap_colmap.keys())
        assert set(df.columns) == set(self.x._playeridmap_colmap.keys())

        assert not df.isna().all().any()            # Check for columns of exclusively NaN
        assert not df.isna().all(axis=1).any()      # Check for rows of exclusively NaN

    def test_playeridmap(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap.playeridmap`.
        """
        # Check that the dictionary of column mappings matches with the column ordering
        assert set(self.x._playeridmap_colmap.values()) == set(self.x._playeridmap_columns)
        assert len(self.x._playeridmap_colmap) == len(self.x._playeridmap_columns)

        # Check that the `DataFrame` columns match with the column ordering
        playeridmap = self.x.playeridmap
        assert set(playeridmap.columns) == set(self.x._playeridmap_columns)
        assert len(playeridmap.columns) == len(self.x._playeridmap_columns)
        assert list(playeridmap.columns) == list(self.x._playeridmap_columns)

        # Check that no columns or rows are exclusively NaN
        assert not playeridmap.isna().all().any()
        assert not playeridmap.isna().all(axis=1).any()

        # Check `dtype` of column values
        assert all(isinstance(x, datetime.datetime) for x in playeridmap["Birthdate"])
        assert all(isinstance(x, list) for x in playeridmap["AllPositions"])
        assert all(isinstance(x, bool) for x in playeridmap["Active"])
        assert all(
            all(isinstance(x, int) for x in playeridmap[c])
            for c in self.x._integer_columns
        )

    def test_changelog_table(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap._changelog_table`.
        """
        table = self.x._changelog_table
        assert table is not None

        dataframes = pd.read_html(str(table))
        assert len(dataframes) == 1

    def test_changelog_dataframe(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap._changelog_dataframe`.
        """
        df = self.x._changelog_dataframe
        assert len(df.columns) == len(self.x._changelog_colmap.keys())
        assert set(df.columns) == set(self.x._changelog_colmap.keys())

        assert not df.isna().all().any()            # Check for columns of exclusively NaN
        assert not df.isna().all(axis=1).any()      # Check for rows of exclusively NaN

    def test_changelog(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb.tools.PlayerIDMap.changelog`.
        """
        assert len(self.x._changelog_colmap) == len(self.x._changelog_columns)
        assert set(self.x._changelog_colmap.values()) == set(self.x._changelog_columns)

        changelog = self.x.changelog
        assert len(changelog.columns) == len(self.x._changelog_columns)
        assert set(changelog.columns) == set(self.x._changelog_columns)

        assert not changelog.isna().all().any()             # Check for columns of exclusively NaN
        assert not changelog.isna().all(axis=1).any()       # Check for rows of exclusively NaN

    @pytest.mark.parametrize(
        "dest", [
            pathlib.Path(".", "PlayerIDMap.xlsx")
        ]
    )
    def test_download_excel(self, dest: pathlib.Path):
        """
        Unit test for :py:meth:`sabrmetrics.sfbb.tools.PlayerIDMap.download_excel`.
        """
        path = self.x.download_excel(dest)
        assert path == dest

        os.remove(dest)

    @pytest.mark.parametrize(
        "dest", [
            pathlib.Path(".", "PlayerIDMap.csv")
        ]
    )
    def test_download_csv(self, dest: pathlib.Path):
        """
        Unit test for :py:meth:`sabrmetrics.sfbb.tools.PlayerIDMap.download_csv`.
        """
        path = self.x.download_csv(dest)
        assert path == dest

        os.remove(dest)

    @pytest.mark.parametrize(
        "dest", [
            pathlib.Path(".", "PlayerIDMap_CHANGELOG.csv")
        ]
    )
    def test_download_csv(self, dest: pathlib.Path):
        """
        Unit test for :py:meth:`sabrmetrics.sfbb.tools.PlayerIDMap.download_changelog_csv`.
        """
        path = self.x.download_changelog_csv(dest)
        assert path == dest

        os.remove(dest)
