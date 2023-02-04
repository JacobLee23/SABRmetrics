"""
"""

import dataclasses


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
            xtype = cls.Fields.__annotations__[k]
            if v is not None and not isinstance(v, xtype):
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
    def default(cls) -> str:
        """
        :return:
        """
        return cls.concatenate(cls.Fields())
