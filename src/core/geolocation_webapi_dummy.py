"""
Author: arcsi1989
"""
from typing import Dict
import warnings

from src.interfaces.geolocation_repository import GeoLocationRepository
from src.common.types import PostalAddress, GeoLocation


class GeoLocationWebAPIDummy(GeoLocationRepository):
    """Implements dummy GeoLocation WebAPI as mock"""
    def __init__(self, config: Dict):
        super().__init__(config=config)

    def geolocation_from_postal_address(self, postal_address: PostalAddress) -> GeoLocation:
        """Post request to the given server address and return a GeoLocation"""
        if isinstance(postal_address, PostalAddress):
            return GeoLocation(12.0, 13.0)
        else:
            warnings.warn(f"Received type: {type(postal_address)} instead of type: PostalAddress")
            return GeoLocation(0., 0.)
