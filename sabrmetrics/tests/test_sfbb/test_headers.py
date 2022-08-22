"""
Tests for :py:mod:`sabrmetrics.sfbb._headers`.
"""

from sabrmetrics.sfbb import _headers


def test_path():
    """

    """
    assert _headers.PATH.exists()
    assert _headers.PATH.suffix == ".json"
