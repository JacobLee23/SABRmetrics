"""
Tests for :py:mod:`sabrmetrics.sfbb._headers`.
"""

import pathlib

import pytest
import requests

from sabrmetrics.sfbb import _headers


class TestHeaders:
    """
    Tests for :py:class:`sabrmetrics.sfbb._headers.Headers`.
    """
    x = _headers.Headers()

    _headers_list_path = pathlib.Path("sabrmetrics", "tests", "test_sfbb", "headers_list.txt")
    with open(_headers_list_path, "r", encoding="utf-8") as file:
        headers_list = file.read().split("\n")

    def test_path(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb._headers.Headers.path`.
        """
        assert self.x.path.exists()
        assert self.x.path.suffix == ".json"

    def test_content(self):
        """
        Unit test for :py:attr:`sabrmetrics.sfbb._headers.Headers.content`.
        """
        assert isinstance(self.x.content, dict)
        assert all(isinstance(k, str) for k in self.x.content.keys())
        assert all(isinstance(v, str) for v in self.x.content.values())

        assert all(k in self.headers_list for k in self.x.content.keys())


@pytest.mark.parametrize(
    "url", [
        "https://baseball-reference.com",
        "https://baseballsavant.mlb.com",
        "https://fangraphs.com",
        "https://github.com",
        "https://github.com/JacobLee23/SABRmetrics",
        "https://google.com",
        "https://mlb.com",
        "https://pypi.org",
        "https://pypi.org/project/sabrmetrics",
        "https://smartfantasybaseball.com",
    ]
)
def test_headers(url: str):
    """
    Unit test for :py:const:`sabrmetrics.sfbb._headers.HEADERS`.

    Regression test for :py:class:`sabrmetrics.sfbb._headers.Headers`.
    """
    with requests.get(url, headers=_headers.HEADERS) as response:
        assert response.status_code == 200, url
