"""

"""


class URLs:
    """

    """
    def __init__(self):
        self._base_address = "https://www.baseball-reference.com"
        self._base_url = "https://www.baseball-reference.com/"

        # players
        self._player_index = "players/{letter}/"
        self._player = "players/{letter}/{player_id}.shtml"

    @property
    def base_address(self) -> str:
        return self._base_address

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def player_index(self) -> str:
        return self._base_url + self._player_index

    @property
    def player(self) -> str:
        return self._base_url + self._player
