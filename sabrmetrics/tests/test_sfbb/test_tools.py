"""
Tests for :py:mod:`sabrmetrics.sfbb.tools`.
"""

import pytest
import requests

from sabrmetrics.sfbb import tools


def test_url():
    """

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
