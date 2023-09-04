"""
"""

from .address import APIAddress
from .scraper import APIScraper


class Address(APIAddress):
    """
    """
    url = "https://statsapi.mlb.com/api/v1/divisions/{division_id}"
    field_defaults = {}


class Division(APIScraper):
    """
    """
    division_id: int

    def __init__(self):
        address = Address()
        address.url = Address.url.format(division_id=self.division_id)

        super().__init__(address)


class ALWest(Division):
    """
    """
    division_id = 200


class ALEast(Division):
    """
    """
    division_id = 201


class ALCentral(Division):
    """
    """
    division_id = 202


class NLWest(Division):
    """
    """
    division_id = 203


class NLEast(Division):
    """
    """
    division_id = 204


class NLCentral(Division):
    """
    """
    division_id = 205
