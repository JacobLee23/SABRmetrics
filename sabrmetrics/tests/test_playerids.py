"""
Tests for :py:mod:`sabrmetrics.playerids`.
"""

import inspect

import pandas as pd
import pytest

from sabrmetrics import playerids


@pytest.mark.parametrize(
    "flavor", [
        x() for x in [
            playerids._SmartFantasyBaseball,
        ]
    ]
)
class TestFlavor:
    """
    Tests for :py:class:`sabrmetrics.playerids.Flavor`.
    """
    def test_name(self, flavor: playerids.Flavor):
        """
        Unit test for :py:attr:`sabrmetrics.playerids.Flavor.name`.
        """
        assert flavor.name

    def test_pid_df(self, flavor: playerids.Flavor):
        """
        Unit test for :py:attr:`sabrmetrics.playerids.Flavor.pid_df`.
        """
        assert not flavor.pid_df.empty, flavor.name

    def test_primary_columns(self, flavor: playerids.Flavor):
        """
        Unit test for :py:attr:`sabrmetrics.playerids.Flavor.primary_columns`.
        """
        assert all(
            x in flavor.pid_df.columns for x in flavor.primary_columns
        ), flavor.name

    def test_site_columns(self, flavor: playerids.Flavor):
        """
        Unit test for :py:attr:`sabrmetrics.playerids.Flavor.site_columns`.
        """
        assert all(
            x in flavor.pid_df.columns for v in flavor.site_columns.values() for x in v
        ), flavor.name


class TestPlayerIDs:
    """
    Tests for :py:class:`sabrmetrics.playerids.PlayerIDs`.
    """
    pids_obj = list(map(playerids.PlayerIDs, playerids.PlayerIDs.flavors()))

    @pytest.mark.parametrize("pids", pids_obj)
    def test_getitem(self, pids: playerids.PlayerIDs):
        """
        Unit test for :py:meth:`sabrmetrics.playerids.PlayerIDs.__getitem__`.
        """
        for name in pids.sites:
            df1 = pids.primary_df
            df2 = pids.site_df(name)
            assert pids[name].equals(pd.concat([df1, df2], axis=1)), (pids, name)

    def test_flavors(self):
        """
        Unit test for :py:meth:`sabrmetrics.playerids.PlayerIDs.flavors`.
        """
        clsmembers = inspect.getmembers(
            playerids, inspect.isclass
        )
        for name, flavor_cls in playerids.PlayerIDs.flavors().items():
            assert (f"_{name}", flavor_cls) in clsmembers, name
            assert issubclass(flavor_cls, playerids.Flavor), name

    def test_get_flavor(self):
        """
        Unit test for :py:meth:`sabrmetrics.playerids.PlayerIDs.get_flavor`.
        """
        for name, _ in playerids.PlayerIDs.flavors().items():
            obj = playerids.PlayerIDs.get_flavor(name)
            assert isinstance(obj, playerids.Flavor), name

        negatives = [
            "DoesNotExist", "RaiseException",
            "BaseballReference", "FanGraphs", "MLB", "Retrosheet"
        ]
        for name in negatives:
            with pytest.raises(KeyError) as err:
                _ = playerids.PlayerIDs.get_flavor(name), (name, err)

    @pytest.mark.parametrize("pids", pids_obj)
    def test_pid_df(self, pids: playerids.PlayerIDs):
        """
        Unit test for :py:attr:`sabrmetrics.playerids.PlayerIDs.pid_df`.
        """
        assert pids.pid_df.equals(pids._flavor.pid_df), pids

    @pytest.mark.parametrize("pids", pids_obj)
    def test_sites(self, pids: playerids.PlayerIDs):
        """
        Unit test for :py:attr:`sabrmetrics.playerids.PlayerIDs.sites`.
        """

    @pytest.mark.parametrize("pids", pids_obj)
    def test_primary_df(self, pids: playerids.PlayerIDs):
        """
        Unit test for :py:attr:`sabrmetrics.playerids.PlayerIDs.primary_df`.
        """
        assert sorted(pids._flavor.primary_columns) == sorted(pids.primary_df.columns), pids

    @pytest.mark.parametrize("pids", pids_obj)
    def test_site_df(self, pids: playerids.PlayerIDs):
        """
        Unit test for :py:meth:`sabrmetrics.playerids.PlayerIDs.site_df`.
        """
        for name in pids.sites:
            df = pids.site_df(name)
            assert not df.empty, name

            assert sorted(df.columns) == sorted(pids._flavor._site_columns[name]), (pids, name)

        negatives = [
            "DoesNotExist", "RaiseException"
        ]
        for name in negatives:
            with pytest.raises(KeyError) as err:
                _ = pids.site_df(name), ((pids, name), err)
