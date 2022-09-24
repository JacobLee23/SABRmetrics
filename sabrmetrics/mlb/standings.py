"""

"""

import collections
import datetime
import typing

import bs4
import requests


class RegularSeason:
    """

    """
    base_address = "https://mlb.com/standings"

    _groups = {"division": "", "league": "league", "mlb": "mlb"}
    groups = collections.namedtuple("StandingsGroups", _groups)(**_groups)

    _levels = {"standard": "", "advanced": "advanced-splits"}
    levels = collections.namedtuple("StandingsLevels", _levels)(**_levels)

    def __init__(
            self, *,
            date: typing.Optional[datetime.date] = None,
            year: typing.Optional[int] = None,
            group: typing.Optional[str] = None,
            level: typing.Optional[str] = None
    ):
        """
        .. note::
            Argument ``date`` takes precedence over argument ``year``.

        .. note::
            Argument ``year`` and the year component of argument ``date`` must be
            greater than or equal to 1901 and less than or equal to the current year

        .. note::
            Invalid values for ``date`` are handled internally by the MLB website API.

            If ``date`` precedes the first day of the regular season of ``year``,
            then ``date`` defaults to the first day of the regular season.
            If the season has not yet been completed and ``date`` succeeds the present day,
            then ``date`` defaults to the present day.
            If ``date`` succeeds the last day of the regular season of ``year``,
            then ``date`` defaults to the last day of the regular season.

            For example:

            - ``2022-01-01`` defaults to ``2022-04-07`` (Opening Day of the 2022 regular season)
            - ``2022-12-31`` defaults to ``2022-10-02`` (Final Day of the 2022 regular season)

            But, on ``2022-04-20``, ``2022-12-31`` defaults to ``2022-04-20``.

            However, an invalid year component of argument ``date`` results in ``HTTP 404``.

        :param date:
        :param year:
        :param group:
        :param level:
        """
        self._address = self.base_address

        if group is not None and isinstance(group, str):
            if group not in self._groups.values():
                raise ValueError("invalid argument 'group' for standings input")
            self._address += f"/{group}"
        if level is not None and isinstance(level, str):
            if level not in self._levels.values():
                raise ValueError("invalid argument 'level' for standings input")
            self._address += f"/{level}"
        if date is not None and isinstance(date, datetime.date):
            if date.year < 1901 or date.year > datetime.date.today().year:
                raise ValueError(f"invalid argument 'date' for standings input: '{date}'")
            self._address += f"/{date.strftime('%Y-%m-%d')}"
        elif year is not None and isinstance(year, int):
            if year < 1901 or year > datetime.datetime.today().year:
                raise ValueError(f"invalid argument 'year' for standings input: '{year}'")
            self._address += f"/{year}"

    @property
    def address(self) -> str:
        """

        :return:
        """
        return self._address

    @property
    def response(self) -> requests.Response:
        """

        :return:
        """
        return requests.get(self.address)

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """

        :return:
        """
        return bs4.BeautifulSoup(self.response.text, features="lxml")
