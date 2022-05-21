"""

"""

import os

import requests

from _sfbb import HEADERS
from _sfbb import SFBBTools


class IDMap:
    """

    """
    _integer_columns = [
        "BaseballHQID", "BaseballProspectusID", "CBSID", "ESPNID", "FanduelID",
        "MLBID", "NFBCID", "OttoneuID", "RotowireID", "YahooID"
    ]

    def __init__(self):
        self._sfbb = SFBBTools()

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
