"""
Scraper for the `Tools`_ page of the **Smart Fantasy Baseball** website.

.. py:data:: HEADERS
    :type: dict
    :canonical: sabrmetrics.sfbb._headers

.. py:data:: URL
    :type: str
    :value: https://smartfantasybaseball.com/tools/

.. _Tools: https://smartfantasybaseball.com/tools/
"""

import datetime
import pathlib
import typing

import bs4
import pandas as pd
import requests

from sabrmetrics.sfbb._headers import HEADERS


URL = "https://www.smartfantasybaseball.com/tools/"


class PlayerIDMap:
    """
    Scraper for the **Player ID Map** section of the Smart Fantasy Baseball _Tools_ webpage.
    """

    _changelog_colmap = {
        "DATE": "Date",
        "DESCRIPTION OF CHANGE": "Description",
    }
    _changelog_columns = [
        "Date", "Description"
    ]

    class IDMaps(typing.NamedTuple):
        """
        A ``NamedTuple`` that contains the URL addresses to download/view the Player ID Map.

        .. py:attribute:: webview

            URL address to view the Player ID Map in a web browser.

            :type: str

        .. py:attribute:: excel_download

            URL address to download the Player ID Map as an Excel Workbook (``.xlsx``).

            :type: str

        .. py:attribute:: csv_download

            URL address to download the Player ID Map as a CSV file (``.csv``).

            :type: str

        .. py:attribute:: changelog_webview

            URL address to view the Player ID Map _CHANGELOG_ in a web browser.

            :type: str

        .. py:attribute:: changelog_csv_download

            URL address to download the Player ID Map _CHANGELOG_ as a CSV file (``.csv``).

            :type: str
        """
        webview: str
        excel_download: str
        csv_download: str

        changelog_webview: str
        changelog_csv_download: str

    @property
    def headers(self) -> dict[str, str]:
        """
        :return: A dictionary of HTTP request headers
        """
        return HEADERS

    @property
    def response(self) -> requests.Response:
        """
        Sends an HTTP GET request to :py:const:`URL`.
        Uses the request headers defined by :py:attr:`Headers.headers`.

        :return: The browser response to the HTTP GET request
        """
        return requests.get(URL, headers=self.headers)

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """
        Parses the request HTML response body.

        :return: The parsed HTML document
        """
        return bs4.BeautifulSoup(self.response.text, features="lxml")

    @property
    def id_maps(self) -> IDMaps:
        """
        Scrapes the hyperlinks for viewing/downloading the Player ID Map.

        :return: A :py:class:`PlayerIDMap.IDMaps` object containing the Player ID Map hyperlinks.
        """
        css = "#content table tr:nth-of-type(2) td:nth-of-type(1) a"

        hyperlinks = [e.attrs.get("href") for e in self.soup.select(css)]
        return self.IDMaps(
            webview=hyperlinks[1], excel_download=hyperlinks[0], csv_download=hyperlinks[2],
            changelog_webview=hyperlinks[3], changelog_csv_download=hyperlinks[4]
        )

    @property
    def _changelog_table(self) -> bs4.Tag:
        """

        :return:
        """
        css = "div#sheets-viewport div.grid-container table"

        with requests.get(self.id_maps.changelog_webview, headers=self.headers) as response:
            soup = bs4.BeautifulSoup(response.text, features="lxml")

        return soup.select_one(css)

    @property
    def _changelog_dataframe(self) -> pd.DataFrame:
        """

        :return:
        """
        dataframes = pd.read_html(str(self._changelog_table))

        df = dataframes[0].iloc[1:, 1:].copy()
        df.columns = dataframes[0].iloc[0, 1:]
        return df

    @property
    def changelog(self) -> pd.DataFrame:
        """

        :return:
        """
        df = self._changelog_dataframe
        df.rename(columns=self._changelog_colmap, inplace=True)
        df = df[self._changelog_columns]

        df["Date"] = df["Date"].apply(
            lambda x: datetime.datetime.strptime(x, "%m/%d/%Y")
        )

        return df

    def download_excel(self, dest: typing.Union[str, pathlib.Path]) -> pathlib.Path:
        """
        Writes the content of the Player ID Map Excel Workbook to a file.
        The location of the generated file is determined by ``dest``.

        :param dest: The file path to write the Player ID Map contents
        :return: The file path to the created file
        :raise ValueError: Invalid file type of ``dest``
        """
        path = pathlib.Path(dest)
        if path.suffix != ".xlsx":
            raise ValueError(
                f"Expected file extension '.xlsx' (Received '{path.suffix}')"
            )

        response = requests.get(self.id_maps.excel_download, headers=HEADERS)
        with open(path, "wb") as file:
            file.write(response.content)

        return path

    def download_csv(self, dest: typing.Union[str, pathlib.Path]) -> pathlib.Path:
        """
        Writes the content of the Player ID Map CSV to a file.
        The location of the generated file is determined by ``dest``.

        :param dest: The file path to write the Player ID Map contents
        :return: The file path to the created file
        :raise ValueError: Invalid file type of ``dest``
        """
        path = pathlib.Path(dest)
        if path.suffix != ".csv":
            raise ValueError(
                f"Expected file extension '.csv' (Received '{path.suffix}')"
            )

        response = requests.get(self.id_maps.csv_download, headers=HEADERS)
        with open(path, "wb") as file:
            file.write(response.content)

        return path

    def download_changelog_csv(self, dest: typing.Union[str, pathlib.Path]) -> pathlib.Path:
        """
        Writes the content of the Player ID Map _CHANGELOG_ CSV to a file.
        The location of the generated file is determined by ``dest``.

        :param dest: The file path to write the Player ID Map _CHANGELOG_ contents
        :return: The file path to the created file
        :raise ValueError: Invalid file type of ``dest``
        """
        path = pathlib.Path(dest)
        if path.suffix != ".csv":
            raise ValueError(
                f"Expected file extension '.csv' (Received '{path.suffix}')"
            )

        response = requests.get(self.id_maps.changelog_csv_download, headers=HEADERS)
        with open(path, "wb") as file:
            file.write(response.content)

        return path
