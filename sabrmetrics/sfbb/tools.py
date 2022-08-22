"""

"""

import bs4
import requests

from sabrmetrics.sfbb._headers import HEADERS


URL = "https://www.smartfantasybaseball.com/tools/"


class PlayerIDMap:
    """

    """
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
