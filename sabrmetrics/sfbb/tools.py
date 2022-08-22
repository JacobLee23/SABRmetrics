"""

"""

import typing

import bs4
import requests

from sabrmetrics.sfbb._headers import HEADERS


URL = "https://www.smartfantasybaseball.com/tools/"


class PlayerIDMap:
    """

    """

    class IDMaps(typing.NamedTuple):
        """

        """
        webview: str
        excel_download: str
        csv_download: str

        changelog_webview: str
        changelog_csv_download: str

    @property
    def headers(self) -> dict[str, str]:
        """

        :return:
        """
        return HEADERS

    @property
    def response(self) -> requests.Response:
        """

        :return:
        """
        return requests.get(URL, headers=self.headers)

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """

        :return:
        """
        return bs4.BeautifulSoup(self.response.text, features="lxml")

    @property
    def id_maps(self) -> IDMaps:
        """

        :return:
        """
        css = "#content table tr:nth-of-type(2) td:nth-of-type(1) a"

        hyperlinks = [e.attrs.get("href") for e in self.soup.select(css)]
        return self.IDMaps(
            webview=hyperlinks[1], excel_download=hyperlinks[0], csv_download=hyperlinks[2],
            changelog_webview=hyperlinks[3], changelog_csv_download=hyperlinks[4]
        )
