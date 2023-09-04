"""
Web scraper for the `Tools`_ page of the **Smart Fantasy Baseball** website.
"""

import datetime
import math
import typing

import bs4
import dateutil.parser
import pandas as pd
import requests


class PlayerIDMap:
    """
    Web scraper for the "Player ID Map" section of the **Smart Fantasy Baseball** _Tools_ webpage.
    
    .. py:attribute:: url

        URL of the _Tools_ page of the **Smart Fantasy Baseball** website.

        :type: str

    .. py:attribute:: headers

        HTTP request headers used for scraping the **Smart Fantasy Baseball** website.

        :type: dict[str, str]

    .. py:attribute:: playeridmap_colmap

        Maps the original Player ID Map ``DataFrame`` column names to the column names of the
        ``DataFrame`` returned by :py:attr:`PlayerIDMap.playeridmap`.

        :type: dict[str, str]
    
    .. py:attribute:: playeridmap_columns

        Determines the order of the columns of the ``DataFrame`` returned by
        :py:attr:`PlayerIDMap.playeridmap`.

        :type: list[str]

    .. py:attribute:: changelog_colmap

        Maps the original Player ID Map CHANGELOG ``DataFrame`` column names to the column names of
        the ``DataFrame`` returned by :py:attr:`PlayerIDMap.changelog`.

        :type: dict[str, str]

    .. py:attribute:: changelog_columns

        Determines the order of the columns of the ``DataFrame`` returned by
        :py:attr:`PlayerIDMap.changelog`.

        :type: list[str]

    .. py:attribute:: primary_columns

        :type: list[str]

    .. py:attribute:: site_columns

        :type: dict[str, list[str]]
    """
    url = "https://smartfantasybaseball.com/tools/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    playeridmap_colmap = {
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
    playeridmap_columns = [
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

    changelog_colmap = {"DATE": "Date", "DESCRIPTION OF CHANGE": "Description"}
    changelog_columns = ["Date", "Description"]

    primary_columns = [
        "PlayerID", "Name", "LastName", "FirstName", "LastFirst", "Birthdate", "Team", "League",
        "Position", "AllPositions", "Bats", "Throws", "Active"
    ]
    site_columns = {
        "BaseballHQ": ["BaseballHQID"], "BaseballProspectus": ["BaseballProspectusID"],
        "BaseballReference": ["BaseballReferenceID"], "CBS": ["CBSID", "CBSName"],
        "ClayDavenport": ["ClayDavenportID"], "DraftKings": ["DraftKingsName"],
        "ESPN": ["ESPNID", "ESPNName"], "FanDuel": ["FanDuelID", "FanDuelName"],
        "FanGraphs": ["FanGraphsID", "FanGraphsName"], "FantasyPros": ["FantasyProsName"],
        "FanTrax": ["FantraxID"], "KFFL": ["KFFLName"], "Masterball": ["MasterballName"],
        "MLB": ["MLBID", "MLBName"], "NFBC": ["NFBCID", "NFBCName", "NFBCLastFirst"],
        "Ottoneu": ["OttoneuID"], "Razzball": ["RazzballName"], "Retrosheet": ["RetrosheetID"],
        "RotoWire": ["RotoWireID", "RotoWireName"], "Yahoo": ["YahooID", "YahooName"],
    }

    def __init__(self):
        with requests.get(self.url, headers=self.headers, timeout=100) as response:
            self._soup = bs4.BeautifulSoup(response.text, features="lxml")

        self._hyperlinks = [
            e.attrs.get("href") for e in self._soup.select(
                "#content table tr:nth-of-type(2) td:nth-of-type(1) a"
            )
        ]

    @property
    def id_maps(self) -> typing.Dict[str, str]:
        """
        Hyperlinks for viewing/downloading the Player ID Map and related files.
        """
        hyperlinks = [
            e.attrs.get("href") for e in self._soup.select(
                "#content table tr:nth-of-type(2) td:nth-of-type(1) a"
            )
        ]
        return {
            "webview": hyperlinks[1], "excel_download": hyperlinks[0],
            "csv_download": hyperlinks[2], "changelog_webview": hyperlinks[3],
            "changelog_csv_download": hyperlinks[4]
        }
    
    @property
    def playeridmap(self) -> pd.DataFrame:
        """
        The content of the Player ID Map table.
        """
        with requests.get(self.id_maps["webview"], headers=self.headers) as response:
            soup = bs4.BeautifulSoup(response.text, features="lxml")
            table = soup.select_one("div#sheets-viewport div.grid-container table")
            dataframes = pd.read_html(str(table))

        df = pd.concat(
            [dataframes[0].iloc[2:, 1:9].copy(), dataframes[0].iloc[2:, 10:].copy()],
            axis=1
        )
        df.columns = [*dataframes[0].iloc[0, 1:9], *dataframes[0].iloc[0, 10:]]
        df.reset_index(drop=True, inplace=True)
        df.rename(columns=self.playeridmap_colmap, inplace=True)
        df = df.loc[:, self.playeridmap_columns]

        integer_columns = [
            "BaseballHQID", "BaseballProspectusID", "CBSID", "ESPNID", "FanDuelID",
            "MLBID", "NFBCID", "OttoneuID", "RotoWireID", "YahooID"
        ]
        df.loc[:, "Birthdate"] = df.loc[:, "Birthdate"].apply(dateutil.parser.parse)
        df.loc[:, "AllPositions"] = df.loc[:, "AllPositions"].apply(lambda x: x.split("/"))
        df.loc[:, "Active"] = df.loc[:, "Active"].apply(lambda x: x == "Y")
        df.loc[:, integer_columns] = df.loc[:, integer_columns].apply(
            lambda s: s.apply(lambda x: pd.NA if math.isnan(x) else int(x))
        )

        return df
    
    @property
    def changelog(self) -> pd.DataFrame:
        """
        The contents of the Player ID Map CHANGELOG table.
        """
        with requests.get(self.id_maps["changelog_webview"], headers=self.headers) as response:
            soup = bs4.BeautifulSoup(response.text, features="lxml")
            table = soup.select_one("div#sheets-viewport div.grid-container table")
            dataframes = pd.read_html(str(table))

        df = dataframes[0].iloc[1:, 1:].copy()
        df.columns = list(dataframes[0].iloc[0, 1:])
        df.reset_index(drop=True, inplace=True)
        df.rename(columns=self.changelog_colmap, inplace=True)
        df = df.loc[:, self.changelog_columns]

        df.loc[:, "Date"] = df.loc[:, "Date"].apply(
            lambda x: datetime.datetime.strptime(x, "%m/%d/%Y")
        )

        return df
