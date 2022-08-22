"""

"""

import json
import pathlib


class Headers:
    """

    """
    @property
    def path(self) -> pathlib.Path:
        """

        :return:
        """
        return pathlib.Path("sabrmetrics", "sfbb", "data", "headers.json")

    @property
    def content(self) -> dict:
        """

        :return:
        """
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)


HEADERS = Headers().content
