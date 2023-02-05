"""
Unit tests for :py:mod:`sabrmetrics.mlb.address`.
"""

import typing

import pytest

from sabrmetrics.mlb import address


class TestAddress_:
    """
    Unit tests for :py:class:`address.Address_`.
    """
    @pytest.mark.parametrize(
        "xtype", [
            dict, float, int, list, set,
            tuple,

            typing.Callable, typing.Dict, typing.DefaultDict, typing.Collection, typing.Generator,
            typing.Iterable, typing.List, typing.Reversible, typing.Sequence, typing.Set,
            typing.Tuple, typing.Type,

            typing.Dict[typing.Any, typing.Any],
            typing.DefaultDict[typing.Any, typing.Any],
            typing.Iterable[typing.Any],
            typing.List[typing.Any],
            typing.Sequence[typing.Any],
            typing.Set[typing.Any],
            typing.Tuple[typing.Any]
        ]
    )
    def test_validate_value_type(self, xtype: typing.Union[type, typing._BaseGenericAlias]):
        """
        Unit test for :py:meth:`address.Address_.validate_value_type`.
        """
        assert isinstance(xtype, (type, typing._BaseGenericAlias))
