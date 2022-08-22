"""
Tests for :py:mod:`sabrmetrics.sfbb.tools`.
"""

import requests

from sabrmetrics.sfbb import tools


def test_url():
    """

    """
    with requests.get(tools.URL, headers=tools.HEADERS) as response:
        assert response.status_code == 200
