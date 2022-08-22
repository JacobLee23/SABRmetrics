"""
Configures the request headers of HTTP GET requests sent to the `Smart Fantasy Baseball`_ website.

.. py:data:: HEADERS

    See :py:attr:`Headers.content`.

.. _Smart Fantasy Baseball: https://smartfantasybaseball.com/
"""

import json
import pathlib


class Headers:
    """
    HTTP GET requests cannot be made to the `Smart Fantasy Baseball`_ website normally.
    Attempting to do so results in a browser response with `status code 406`_.

    .. code-block:: python

        >>> import requests
        >>> requests.get("https://smartfantasybaseball.com/")
        <Response [406]>

    Thus, the following HTTP request headers are set when making the GET request:

    - ``User-Agent``

    After instantiating a :py:class:`Headers` object,
    the :py:attr:`Headers.content` property can be passed as the
    ``headers`` argument of the ``requests.get()`` function call:

    .. code-block:: python

        >>> import requests
        >>> from sabrmetrics.sfbb._headers import Headers
        >>> request_headers = Headers()
        >>> requests.get("https://smartfantasybaseball.com/", headers=request_headers.content)
        <Response [200]>

    .. _Smart Fantasy Baseball: https://smartfantasybaseball.com/
    .. _status code 406: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
    """
    @property
    def path(self) -> pathlib.Path:
        """
        :return: The path to the JSON file containing the HTTP request headers
        """
        return pathlib.Path("sabrmetrics", "sfbb", "data", "headers.json")

    @property
    def content(self) -> dict[str, str]:
        """
        Reads the file containing the JSON-serialized dictionary of HTTP request headers.
        De-serializes the file contents to be Python-readable.

        :return: The HTTP request headers
        """
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)


HEADERS = Headers().content
