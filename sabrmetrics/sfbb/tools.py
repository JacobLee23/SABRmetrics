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
import math
import pathlib
import typing

import bs4
import dateutil.parser
import pandas as pd
import requests

from sabrmetrics.sfbb._headers import HEADERS

URL = "https://www.smartfantasybaseball.com/tools/"


class PlayerIDMap:
    """
    Scraper for the **Player ID Map** section of the Smart Fantasy Baseball *Tools* webpage.
    """

    # Maps the original Player ID Map `DataFrame` column names to the column names of the
    # `DataFrame` returned by :py:attr:`PlayerIDMap.playeridmap`.
    _playeridmap_colmap = {
        "IDPLAYER": "PlayerID", "PLAYERNAME": "Name", "BIRTHDATE": "Birthdate",
        "FIRSTNAME": "FirstName", "LASTNAME": "LastName", "TEAM": "Team",
        "LG": "League", "POS": "Position", "IDFANGRAPHS": "FanGraphsID",
        "FANGRAPHSNAME": "FanGraphsName", "MLBID": "MLBID", "MLBNAME": "MLBName",
        "CBSID": "CBSID", "CBSNAME": "CBSName", "RETROID": "RetrosheetID",
        "BREFID": "BaseballReferenceID", "NFBCID": "NFBCID", "NFBCNAME": "NFBCName",
        "ESPNID": "ESPNID", "ESPNNAME": "ESPNName", "KFFLNAME": "KFFLName",
        "DAVENPORTID": "ClayDavenportID", "BPID": "BaseballProspectusID", "YAHOOID": "YahooID",
        "YAHOONAME": "YahooName", "MSTRBLLNAME": "MasterballName", "BATS": "Bats",
        "THROWS": "Throws", "FANTPROSNAME": "FantasyProsName", "LASTCOMMAFIRST": "LastFirst",
        "ROTOWIREID": "RotoWireID", "FANDUELNAME": "FanDuelName", "FANDUELID": "FanDuelID",
        "DRAFTKINGSNAME": "DraftKingsName", "OTTONEUID": "OttoneuID", "HQID": "BaseballHQID",
        "RAZZBALLNAME": "RazzballName", "FANTRAXID": "FantraxID", "FANTRAXNAME": "FantraxName",
        "ROTOWIRENAME": "RotoWireName", "ALLPOS": "AllPositions", "NFBCLASTFIRST": "NFBCLastFirst",
        "ACTIVE": "Active",
    }
    # Determines the order of the columns of the `DataFrame` returned by
    # :py:attr:`PlayerIDMap.playeridmap`.
    _playeridmap_columns = [
        "PlayerID", "Name", "LastName", "FirstName", "LastFirst",
        "Birthdate", "Team", "League", "Position", "AllPositions",
        "Bats", "Throws", "Active",

        "BaseballHQID", "BaseballProspectusID", "BaseballReferenceID", "ClayDavenportID", "CBSID",
        "CBSName", "DraftKingsName", "ESPNID", "ESPNName", "FanDuelID",
        "FanDuelName", "FanGraphsID", "FanGraphsName", "FantasyProsName", "FantraxID",
        "FantraxName", "KFFLName", "MasterballName", "MLBID", "MLBName",
        "NFBCID", "NFBCName", "NFBCLastFirst", "OttoneuID", "RazzballName",
        "RetrosheetID", "RotoWireID", "RotoWireName", "YahooID", "YahooName",
    ]

    # Maps the original Player ID Map CHANGELOG `DataFrame` column names to the column names of the
    # `DataFrame` returned by :py:attr:`PlayerIDMap.changelog`.
    _changelog_colmap = {
        "DATE": "Date", "DESCRIPTION OF CHANGE": "Description",
    }
    # Determines the order of the columns of the `DataFrame` returned by
    # :py:attr:`PlayerIDMap.changelog`.
    _changelog_columns = [
        "Date", "Description"
    ]

    # Names of the columns of the `DataFrame` returned by :py:attr:`PlayerIDMap.playeridmap` that
    # should be converted to type `int`.
    _integer_columns = [
        "BaseballHQID", "BaseballProspectusID", "CBSID", "ESPNID", "FanDuelID",
        "MLBID", "NFBCID", "OttoneuID", "RotoWireID", "YahooID"
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
    def response(self) -> requests.Response:
        """
        Sends an HTTP GET request to :py:const:`URL`.

        :return: The browser response to the HTTP GET request
        """
        return requests.get(URL, headers=HEADERS)

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
        # CSS selector of the anchor (`<a>`) elements in the 'Player ID Map' section of the Smart
        # Fantasy Baseball 'Tools' webpage.
        css = "#content table tr:nth-of-type(2) td:nth-of-type(1) a"

        # Get the Player ID Map viewing/download URLs from the 'href' attributes of the anchor
        # (`<a>`) elements.
        hyperlinks = [e.attrs.get("href") for e in self.soup.select(css)]
        return self.IDMaps(
            webview=hyperlinks[1], excel_download=hyperlinks[0], csv_download=hyperlinks[2],
            changelog_webview=hyperlinks[3], changelog_csv_download=hyperlinks[4]
        )

    @property
    def _playeridmap_table(self) -> bs4.Tag:
        """
        Scrapes the ``<table>`` element that corresponds to the Player ID Map table.

        :return: The ``<table>`` element on the Player ID Map table
        """
        # CSS selector of the table (`<table>`) element in the Player ID Map webview.
        css = "div#sheets-viewport div.grid-container table"

        # Parse the browser HTML response to an HTTP GET request sent to the Player ID Map webview
        # URL.
        with requests.get(self.id_maps.webview, headers=HEADERS) as response:
            soup = bs4.BeautifulSoup(response.text, features="lxml")

        return soup.select_one(css)

    @property
    def _playeridmap_dataframe(self) -> pd.DataFrame:
        """
        Parses the Player ID Map ``<table>`` element.
        The inner HTML of the ``<table>`` element is read and processed as a ``DataFrame``.

        :return: The ``DataFrame`` representation of the Player ID Map table
        """
        # Generate `DataFrame` objects for each of the table (`<table>`) elements in the Player ID
        # Map webview.
        dataframes = pd.read_html(str(self._playeridmap_table))

        # Create a `DataFrame` object that represents the Player ID Map table.
        #
        # Note the following properties of the Player ID Map `DataFrame` representation:
        # - The row at index 0 is a row of the table column names.
        # - The row at index 1 is a divider and is processed as a row of NaN values.
        # - The column at index 0 is a numbering of the table rows.
        # - The column at index 9 is a divider and is processed as a column of NaN values.
        df = pd.concat(
            [dataframes[0].iloc[2:, 1:9].copy(), dataframes[0].iloc[2:, 10:].copy()],
            axis=1
        )
        df.columns = [*dataframes[0].iloc[0, 1:9], *dataframes[0].iloc[0, 10:]]

        df.reset_index(drop=True, inplace=True)

        return df

    @property
    def playeridmap(self) -> pd.DataFrame:
        """
        Scrapes, reads, and processes the `Player ID Map`_ table.

        The ``DataFrame`` columns are renamed and reordered according to pre-defined operations.
        Additionally, type modifications are performed on selected columns.
        The types of the ``DataFrame`` values are listed below by column name:

        +--------------+-----------------------+
        | Name         | Type                  |
        +==============+=======================+
        | PlayerID     | ``str``               |
        +--------------+-----------------------+
        | Name         | ``str``               |
        +--------------+-----------------------+
        | LastName     | ``str``               |
        +--------------+-----------------------+
        | FirstName    | ``str``               |
        +--------------+-----------------------+
        | LastFirst    | ``str``               |
        +--------------+-----------------------+
        | Birthdate    | ``datetime.datetime`` |
        +--------------+-----------------------+
        | Team         | ``str``               |
        +--------------+-----------------------+
        | League       | ``str``               |
        +--------------+-----------------------+
        | Position     | ``str``               |
        +--------------+-----------------------+
        | AllPositions | ``list[str]``         |
        +--------------+-----------------------+
        | Bats         | ``str``               |
        +--------------+-----------------------+
        | Throws       | ``str``               |
        +--------------+-----------------------+
        | Active       | ``bool``              |
        +--------------+-----------------------+

        Furthermore, the ``DataFrame`` values of the SABRmetrics website columns are listed below:

        - ``int``:
            - BaseballHQID
            - BaseballProspectusID
            - CBSID
            - ESPNID
            - FanDuelID
            - MLBID
            - NFBCID
            - OttoneuID
            - RotoWireID
            - YahooID
        - ``str``:
            - BaseballReferenceID
            - CBSName
            - ClayDaveportID
            - DraftKingsName
            - ESPNName
            - FanDuelName
            - FanGraphsID
            - FanGraphsName
            - FantasyProsName
            - FanTraxID
            - FanTraxName
            - KFFLName
            - MasterballName
            - MLBName
            - NFBCName
            - NFBCLastFirst
            - RazzballName
            - RetrosheetID
            - RotoWireName
            - YahooName

        *Note: All values of the ``DataFrame`` are initially of type ``str``.*

        :return: A ``DataFrame`` representation of the Player ID Map

        .. _Player ID Map: https://www.smartfantasybaseball.com/PLAYERIDMAPWEB
        """
        df = self._playeridmap_dataframe

        # Modify `DataFrame` columns
        df.rename(columns=self._playeridmap_colmap, inplace=True)
        df = df[self._playeridmap_columns]

        # `str` -> `datetime.datetime`
        #
        # Strings adhere to either a '%m/%d/%Y' or '%m/%d/%y' date format.
        # Creating a `datetime.datetime` object from the string would require a `try`/`except`.
        # Instead, we assume that the date format is common and parseable by `dateutil`.
        df["Birthdate"] = df["Birthdate"].apply(
            dateutil.parser.parse
        )
        # `str` -> `list[str]`
        df["AllPositions"] = df["AllPositions"].apply(
            lambda x: x.split("/")
        )
        # `str` -> `bool`
        df["Active"] = df["Active"].apply(
            lambda x: x == "Y"
        )
        # `str` -> `int`
        df[self._integer_columns] = df[self._integer_columns].applymap(
            lambda x: 0 if math.isnan(float(x)) else int(x)
        )

        return df

    @property
    def _changelog_table(self) -> bs4.Tag:
        """
        Scrapes the ``<table>`` element that corresponds to the Player ID Map CHANGELOG table.

        :return: The ``<table>`` element of the CHANGELOG table
        """
        # CSS selector of the table (`<table>`) element in the Player ID Map CHANGELOG webview.
        css = "div#sheets-viewport div.grid-container table"

        # Parse the browser HTML response to an HTTP GET request sent to the Player ID Map
        # CHANGELOG webview URL.
        with requests.get(self.id_maps.changelog_webview, headers=HEADERS) as response:
            soup = bs4.BeautifulSoup(response.text, features="lxml")

        return soup.select_one(css)

    @property
    def _changelog_dataframe(self) -> pd.DataFrame:
        """
        Parses the CHANGELOG ``<table>`` element.
        The inner HTML of the ``<table>`` element is read and processed as a ``DataFrame``.

        :return: The ``DataFrame`` representation of the CHANGELOG table
        """
        # Generate `DataFrame` objects for each of the table (`<table>`) elements in the Player ID
        # Map CHANGELOG webview.
        dataframes = pd.read_html(str(self._changelog_table))

        # Create a `DataFrame` object that represents the Player ID Map table.
        #
        # Note the following properties of the Player ID Map `DataFrame` representation:
        # - The row at index 0 is a row of the table column names.
        # - The column at index 0 is a numbering of the table rows.
        df = dataframes[0].iloc[1:, 1:].copy()
        df.columns = list(dataframes[0].iloc[0, 1:])

        df.reset_index(drop=True, inplace=True)

        return df

    @property
    def changelog(self) -> pd.DataFrame:
        """
        Scrapes, reads, and processes the Player ID Map `CHANGELOG`_ table.

        The ``DataFrame`` columns are renamed and reordered according to pre-defined operations.
        Additionally, type modifications are performed on selected columns.
        The types of the ``DataFrame`` values are listed below by column name:

        +-------------+-------------------------+
        | Name        | Type                    |
        +=============+=========================+
        | Date        | ``datetime.datetime`` * |
        +-------------+-------------------------+
        | Description | ``str``                 |
        +-------------+-------------------------+

        *Note: All values of the ``DataFrame`` are initially of type ``str``.*

        :return: A ``DataFrame`` representation of the Player ID Map CHANGELOG

        .. _CHANGELOG: https://www.smartfantasybaseball.com/PLAYERIDMAPCHANGELOG
        """
        df = self._changelog_dataframe

        # Modify `DataFrame` columns
        df.rename(columns=self._changelog_colmap, inplace=True)
        df = df[self._changelog_columns]

        # `str` -> `datetime.datetime`
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

        # Check that the destination file type corresponds to an Excel Workbook.
        if path.suffix != ".xlsx":
            raise ValueError(
                f"Expected file extension '.xlsx' (Received '{path.suffix}')"
            )

        # Send HTTP GET request to the URL address that downloads the Player ID Map as an Excel
        # Workbook.
        with requests.get(self.id_maps.excel_download, headers=HEADERS) as response:
            # Create/Open Excel Workbook at destination.
            with open(path, "wb") as file:
                # Write browser binary response to destination file.
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

        # Check that the destination file type corresponds to a CSV file.
        if path.suffix != ".csv":
            raise ValueError(
                f"Expected file extension '.csv' (Received '{path.suffix}')"
            )

        # Send HTTP GET request to the URL address that downloads the Player ID Map as a CSV file.
        with requests.get(self.id_maps.csv_download, headers=HEADERS) as response:
            # Create/Open CSV file at destination.
            with open(path, "wb") as file:
                # Write browser binary response to destination file.
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

        # Check that the destination file type corresponds to a CSV file.
        if path.suffix != ".csv":
            raise ValueError(
                f"Expected file extension '.csv' (Received '{path.suffix}')"
            )

        # Send HTTP GET request to the URL address that downloads the Player ID Map CHANGELOG as a
        # CSV file.
        with requests.get(self.id_maps.changelog_csv_download, headers=HEADERS) as response:
            # Create/Open CSV file at destination.
            with open(path, "wb") as file:
                # Write browser binary response to destination file.
                file.write(response.content)

        return path
