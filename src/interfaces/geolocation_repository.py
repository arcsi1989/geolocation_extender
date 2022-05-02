"""
Author: arcsi1989
"""
from abc import ABC, abstractmethod
from typing import Dict

from common.types import PostalAddress, GeoLocation


class GeoLocationRepository(ABC):
    """Implements an interface for location repository"""

    def __init__(self, config: Dict):
        self._config = config

    @abstractmethod
    def geolocation_from_postal_address(self, postal_address: PostalAddress) -> GeoLocation:
        pass
