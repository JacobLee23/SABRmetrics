"""
"""

import typing


class Address_:
    """
    """
    base: str

    class _FieldDefaults(typing.NamedTuple):
        pass

    def __init__(self, **kwargs: typing.Any):
        fields = self.field_defaults()
        for key, value in kwargs.items():
            if key in fields:
                fields[key] = value
        self._fields = fields

        self.check_fields()

    def __getitem__(self, key: str) -> str:
        return self.fields[key]

    @staticmethod
    def check_value_type(
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
    def field_types(cls) -> typing.Dict[str, typing.Union[type, typing._BaseGenericAlias]]:
        """
        :return:
        """
        return {k: cls._FieldDefaults.__annotations__[k] for k in cls._FieldDefaults._fields}

    @classmethod
    def field_defaults(cls) -> typing.Dict[str, typing.Any]:
        """
        :return:
        """
        return cls._FieldDefaults._field_defaults

    @property
    def fields(self) -> typing.Dict[str, str]:
        """
        :return:
        """
        return self._fields

    def check_fields(self):
        """
        :raise TypeError:
        """
        field_types = self.field_types()

        for key, value in self.fields.items():
            if value is None:
                continue

            xtype = field_types[key]
            if not self.check_value_type(value, xtype):
                raise TypeError(
                    f"parameter {key} must be {xtype}, not {type(value)}"
                )

    def concatenate(self) -> str:
        """
        :return:
        """
        raise NotImplementedError
