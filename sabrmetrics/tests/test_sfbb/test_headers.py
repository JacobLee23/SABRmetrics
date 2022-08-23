"""
Tests for :py:mod:`sabrmetrics.sfbb._headers`.
"""

import pytest
import requests

from sabrmetrics.sfbb import _headers


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
