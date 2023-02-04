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

    @classmethod
    def check_address_fields(cls, fields: Fields):
        for k, v in vars(fields).items():
            if v is None:
                continue

            xtype = cls.Fields.__annotations__[k]

            if (
                (
                    isinstance(xtype, type)
                    and not isinstance(v, xtype)
                )
                or (
                    isinstance(xtype, typing._BaseGenericAlias)
                    and not isinstance(v, xtype.__origin__)
                )
            ):
                raise TypeError(
                    f"parameter {k} must be {xtype}, not {type(v)}"
                )
                
    @classmethod
    def concatenate(cls, fields: Fields) -> str:
        """
        :param fields:
        """
        cls.check_address_fields(fields)

        raise NotImplementedError

    @classmethod
    def defaults(cls) -> Fields:
        """
        :return:
        """
        return cls.Fields()
