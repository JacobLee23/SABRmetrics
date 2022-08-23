"""
Configures the request headers of HTTP GET requests sent to the `Smart Fantasy Baseball`_ website.

HTTP Get requests cannot be made to the `Smart Fantasy Baseball`_ website cannot be made normally.
Attempting to do so results in a browser response with `status code 406`_:

.. code-block:: python

    >>> import requests
    >>> requests.get("https://smartfantasybaseball.com/")
    <Response [406]>

Thus, the following HTTP request headers are set when making the GET request:

- ``User-Agent``

The value of :py:data:`HEADERS` can be passed as the ``headers`` argument to ``requests.get()``:

 .. code-block:: python

    >>> import requests
    >>> from sabrmetrics.sfbb._headers import HEADERS
    >>> requests.get("https://smartfantasybaseball.com/", headers=HEADERS)
    <Response [200]>

.. py:data:: PATH

    The path to the JSON file containing the HTTP request headers.

    :type: pathlib.Path

.. py:data:: HEADERS

    The contents of the JSON-serialized dictionary of HTTP request headers at :py:data:`PATH`.

    :type: dict

.. _Smart Fantasy Baseball: https://smartfantasybaseball.com/
.. _status code 406: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
"""

import json
import pathlib


PATH = pathlib.Path("sabrmetrics", "sfbb", "data", "headers.json")
with open(PATH, "r", encoding="utf-8") as file:
    HEADERS = json.load(file)
