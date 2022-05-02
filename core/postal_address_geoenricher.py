"""
Author: arcsi1989
"""

from typing import List, Dict
import multiprocessing as mp
from dataclasses import asdict

from common.types import PostalAddress, GeoLocation
from interfaces import GeoLocationRepository


class PostalAddressGeoEnricher:
    """Implements PostalAddressGeoEnricher - extend the postal address with geo location informations"""
    def __init__(self, geo_repo: GeoLocationRepository):
        self._geo_repo = geo_repo
        self.geo_json_addresses = None

    def enrich_addresses(self, postal_addresses: List[PostalAddress]):
        """Enriches postal addresses with geo-information"""
        num_cores = mp.cpu_count()
        with mp.Pool(num_cores - 1) as pool:
            result = pool.imap(self.create_geo_json_address, postal_addresses, chunksize=1000)
            self.geo_json_addresses = [x for x in result]

    def create_geo_json_address(self, postal_address):
        geo_location = self._geo_repo.geolocation_from_postal_address(postal_address=postal_address)
        if geo_location == GeoLocation(0., 0.):
            return None
        geo_json_address = self.geo_json_formatter(postal_address=postal_address, geo_location=geo_location)
        return geo_json_address

    @staticmethod
    def geo_json_formatter(postal_address: PostalAddress, geo_location: GeoLocation) -> Dict:
        geo_json_dict_address = {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [geo_location.longitude, geo_location.latitude]
          },
        }
        geo_json_dict_address.update({'properties': asdict(postal_address)})
        return geo_json_dict_address




