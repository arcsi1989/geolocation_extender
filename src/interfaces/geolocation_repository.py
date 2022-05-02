"""
Author: arcsi1989
"""
from abc import ABC, abstractmethod
from typing import Dict

from src.common.types import PostalAddress, GeoLocation


class GeoLocationRepository(ABC):
    """
    Implements an abstract geo-location repository functioning as an interface
    """

    def __init__(self, config: Dict):
        self._config = config

    @abstractmethod
    def geolocation_from_postal_address(self, postal_address: PostalAddress) -> GeoLocation:
        """Returns geo-location information based on postal address"""
        pass
