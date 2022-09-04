"""
Wrapper for the various Player ID databases in the codebase.

Supported sites:

- `Smart Fantasy Baseball`_: :py:class:`sabrmetrics.sfbb.tools.PlayerIDMap`

.. _Smart Fantasy Baseball: https://smartfantasybaseball.com/
"""

import typing

import pandas as pd

from sabrmetrics import sfbb


class Flavor:
    """
    Represents the Player ID database of one of the supported websites.
    (See the :py:mod:`sabrmetrics.playerids` documentation for a list of supported websites.
    """
    def __init__(
            self, name: str, pid_df: pd.DataFrame,
            *, primary_columns: list[str], site_columns: dict[str, list[str]]
    ):
        """
        :param name: The name of the website from which the Player ID database is taken
        :param pid_df: The full Player ID ``DataFrame`` defined by the selected website
        :param primary_columns: The ``pid_df`` primary columns
        :param site_columns: The ``pid_df`` columns specific to supported SABRmetrics websites
        """
        self._name = name
        self._pid_df = pid_df

        self._primary_columns = primary_columns
        self._site_columns = site_columns

    def __repr__(self) -> str:
        return f"_Flavor(name='{self.name}')"

    @property
    def name(self) -> str:
        """
        :return: The name of the website from which the Player ID database is taken
        """
        return self._name

    @property
    def pid_df(self) -> pd.DataFrame:
        """
        :return: The full Player ID ``DataFrame`` defined by the selected website
        """
        return self._pid_df

    @property
    def primary_columns(self) -> list[str]:
        """
        The primary columns of the Player ID ``DataFrame`` are universal across all websites.
        They are independent of the website, such as:
        active (i.e., active/inactive); age; batting handedness; birthdate; first name; last name;
        league; name (although some websites have specific formats that are not universal);
        playing position(s); team; throwing handedness.

        :return: The primary columns of :py:attr:`_Flavor.pid_df`
        """
        return self._primary_columns

    @property
    def site_columns(self) -> dict[str, list[str]]:
        """
        The site-specific columns of the Player ID ``DataFrame`` are unique between websites.
        They are largely dependent on the website, such as:
        a site-specific name format; a site-specific identifier (ID).

        :return: The :py:attr:`_Flavor.pid_df` columns specific to supported SABRmetrics websites
        """
        return self._site_columns


class _SmartFantasyBaseball(Flavor):
    """
    Wrapper for :py:class:`sabrmetrics.sfbb.tools.PlayerIDMap`.
    """
    _name = "SmartFantasyBaseball"

    _primary_columns: list[str] = [
        "PlayerID", "Name", "LastName", "FirstName", "LastFirst",
        "Birthdate", "Team", "League", "Position", "AllPositions",
        "Bats", "Throws", "Active"
    ]
    _site_columns: dict[str, list[str]] = {
        "BaseballHQ": ["BaseballHQID"],
        "BaseballProspectus": ["BaseballProspectusID"],
        "BaseballReference": ["BaseballReferenceID"],
        "CBS": ["CBSID", "CBSName"],
        "ClayDavenport": ["ClayDavenportID"],
        "DraftKings": ["DraftKingsName"],
        "ESPN": ["ESPNID", "ESPNName"],
        "FanDuel": ["FanDuelID", "FanDuelName"],
        "FanGraphs": ["FanGraphsID", "FanGraphsName"],
        "FantasyPros": ["FantasyProsName"],
        "FanTrax": ["FantraxID"],
        "KFFL": ["KFFLName"],
        "Masterball": ["MasterballName"],
        "MLB": ["MLBID", "MLBName"],
        "NFBC": ["NFBCID", "NFBCName", "NFBCLastFirst"],
        "Ottoneu": ["OttoneuID"],
        "Razzball": ["RazzballName"],
        "Retrosheet": ["RetrosheetID"],
        "RotoWire": ["RotoWireID", "RotoWireName"],
        "Yahoo": ["YahooID", "YahooName"],
    }

    def __init__(self):
        self._obj = sfbb.tools.PlayerIDMap()

        super().__init__(
            self._name, self._obj.playeridmap,
            primary_columns=self._primary_columns,
            site_columns=self._site_columns
        )


class PlayerIDs:
    """
    Wrapper for :py:class:`Flavor` objects, providing a higher-level API.

    .. note::
        The ``PlayerIDs`` class defines the ``__getitem__`` magic method
        (`documentation <https://docs.python.org/3/reference/datamodel.html#object.__getitem__>`_).
        Indexing a ``PlayerIDs`` object with name of one of the sites supported by the flavor
        returns the primary columns of the Player ID database concatenated with the site-specific
        columns of the Player ID database corresponding to the value passed.
        (A tuple of supported sites is returned by :py:meth:`PlayerIDs.sites`.)

        Sample usage:

        .. code-block:: python
            >>> import typing
            >>> import pandas as pd
            >>> from sabrmetrics import playerids
            >>> flavor: typing.Union[str, playerids.Flavor]     # E.g., "SmartFantasyBaseball"
            >>> pids = playerids.PlayerIDs(flavor)
            >>> site_name: str      # E.g., "BaseballReference", "FanGraphs", "MLB", "Retrosheet"
            >>> df = pids[site_name]
            >>> df1 = pids.primary_df
            >>> df2 = pids.site_df(site_name)
            >>> df.equals(pd.concat([df1, df2], axis=1))
            True
    """
    _flavors: dict[str, type] = {
        "SmartFantasyBaseball": _SmartFantasyBaseball
    }

    def __init__(self, flavor: typing.Union[str, Flavor]):
        """
        :param flavor: A :py:class:`Flavor` object or its corresponding ``name``  property
        """
        if isinstance(flavor, str):
            self._flavor = self.get_flavor(flavor)
        elif isinstance(flavor, Flavor):
            self._flavor = flavor
        else:
            raise TypeError(
                f"Expected str or _Flavor, got {type(flavor)}"
            )

    def __repr__(self) -> str:
        return f"PlayerIDs(_flavor={self._flavor})"

    def __getitem__(self, item: str):
        """
        Let ``pids`` be an instance of ``PlayerIDs``.
        The expression ``pids[item]`` calls the ``pandas.concat`` function
        (`documentation <https://pandas.pydata.org/docs/reference/api/pandas.concat.html>`_)
        to concatenate the ``DataFrame`` object returned by :py:attr:`PlayerIDs.primary_df`
        with the ``DataFrame`` object returned by the call to :py:meth:`PlayerIDs.site_df`,
        (more explicitly, ``pids.site_df(item)``).

        .. note::
            ``item`` is case-sensitive.

        :param item: The name of the site supported by the Player ID database flavor
        :return: The primary columns concatenated with the columns spcific to ``item``
        """
        return pd.concat(
            [self.primary_df, self.site_df(item)],
            axis=1
        )

    @classmethod
    def flavors(cls) -> dict[str, type]:
        """

        :return:
        """
        return cls._flavors

    @classmethod
    def get_flavor(cls, name: str) -> Flavor:
        """
        Instantiates an object of :py:class:`Flavor` such that :py:attr:`name` equals ``name``.

        .. note::
            Argument ``name`` is case-sensitive.

        :param name: The ``name`` property of the :py:class:`Flavor` object
        :return: The :py:class:`Flavor` object corresponding to ``name``
        :raise KeyError: No :py:class:`Flavor` class corresponding to ``name`` could be found
        """
        flavor_cls = cls._flavors[name]
        flavor = flavor_cls()

        return flavor

    @property
    def pid_df(self) -> pd.DataFrame:
        """
        Synonymous to :py:attr:`Flavor.pid_df`.
        """
        return self._flavor.pid_df

    @property
    def sites(self) -> list[str]:
        """
        Returns a list of the names of the websites supported by the specific Player ID database.
        All member elements of the returne tuple can be passed as the ``name`` argument of
        :py:meth:`PlayerIDs.site_df` or as the value used to index the object
        (i.e., the ``item`` parameter of ``PlayerIDs.__getitem__``).

        :return: The names of the supported sites
        """
        return list(self._flavor.site_columns)

    @property
    def primary_df(self) -> pd.DataFrame:
        """
        Indexes :py:meth:`PlayerIDs.pid_df` by the primary columns of the Player ID database.
        The primary columns labels are determined by :py:attr:`Flavor.primary_columns`.

        :return: The primary columns of the PLayer ID database
        """
        return self.pid_df.loc[:, self._flavor.primary_columns]

    def site_df(self, name: str) -> pd.DataFrame:
        """
        Indexes :py:meth:`PlayerIDs.pid_df` by the columns of the Player ID database specific to
        ``name``.
        The site-specific column labels are determiend by :py:attr:`Flavor.site_columns`.

        .. note::
            A list of supported websites whose names can be passed as the ``name`` argument can be
            obtained via :py:attr:`PlayerIDs.sites`.

            Argument ``name`` is case-sensitive.

        :param name: The name of the website
        :return: The site-specific columns of the Player ID database
        :raise KeyError: No supported website corresponding to ``name`` could be found
        """
        columns = self._flavor.site_columns[name]

        return self.pid_df.loc[:, columns]
