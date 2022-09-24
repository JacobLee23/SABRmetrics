"""

"""


class RegularSeason:
    """

    """
    base_address = "https://mlb.com/standings"

    def __init__(self):
        self._address = self.base_address

    @property
    def address(self) -> str:
        """

        :return:
        """
        return self._address
