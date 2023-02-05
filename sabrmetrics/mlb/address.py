"""
"""

import dataclasses
import typing


class Address_:
    """
    .. py:attribute:: base
        :type: str
    """
    base: str

    @dataclasses.dataclass
    class Fields:
        pass

    @staticmethod
    def validate_value_type(
        value: typing.Any, xtype: typing.Union[type, typing._BaseGenericAlias]
    ) -> bool:
        """
        :param value:
        :param xtype:
        :return:
        """
        # `xtype` is a type
        if isinstance(xtype, type) and isinstance(value, xtype):
            return True

        # `xtype` is a typing generic
        if isinstance(xtype, typing._BaseGenericAlias) and isinstance(value, xtype.__origin__):
            return True

        return False


    @classmethod
    def check_address_fields(cls, fields: Fields):
        """
        :param fields:
        :raise TypeError:
        """
        for k, v in vars(fields).items():
            if v is None:
                continue

            # Get arguments of `cls.Fields` and corresponding type annotations
            xtype = cls.Fields.__annotations__[k]

            if not cls.validate_value_type(v, xtype):
                raise TypeError(
                    f"parameter {k} must be {xtype}, not {type(v)}"
                )
            
                
    @classmethod
    def concatenate(cls, fields: Fields) -> str:
        """
        :param fields:
        :return:
        """
        cls.check_address_fields(fields)

        raise NotImplementedError

    @classmethod
    def defaults(cls) -> Fields:
        """
        :return:
        """
        return cls.Fields()
