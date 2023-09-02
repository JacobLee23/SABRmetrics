"""
"""

import typing


class APIAddress:
    """
    """
    url: str
    field_defaults: typing.Dict[str, typing.Any]

    def __init__(self, **kwargs: typing.Any):
        self._fields = {}
        for key, value in self.field_defaults.items():
            self._fields.setdefault(
                key,
                kwargs[key] if key in filter(lambda x: kwargs[x] is not None, kwargs) else value
            )

    def __repr__(self) -> str:
        arguments = ", ".join(f"{k}={self.__getattribute__(k)}" for k in self.fields)
        return f"{type(self).__name__}({arguments})"

    @property
    def fields(self) -> typing.Dict[str, typing.Any]:
        """
        """
        return self._fields
    
    @property
    def parameters(self) -> typing.Dict[str, str]:
        """
        """
        raise NotImplementedError
