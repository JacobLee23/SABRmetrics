"""
Tests for :py:mod:`sabrmetrics.sfbb._headers`.
"""

import pathlib

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
        Test for :py:attr:`sabrmetrics.sfbb._headers.Headers.path`.
        """
        assert self.x.path.exists()
        assert self.x.path.suffix == ".json"

    def test_content(self):
        """
        Test for :py:attr:`sabrmetrics.sfbb._headers.Headers.content`.
        """
        assert isinstance(self.x.content, dict)
        assert all(isinstance(k, str) for k in self.x.content.keys())
        assert all(isinstance(v, str) for v in self.x.content.values())

        assert all(k in self.headers_list for k in self.x.content.keys())
