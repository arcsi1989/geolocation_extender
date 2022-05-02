"""
Author: arcsi1989
"""
from typing import Dict
import warnings

import requests
import json
from dataclasses import asdict

from interfaces.geolocation_repository import GeoLocationRepository
from common.types import PostalAddress, GeoLocation


class GeoLocationWebAPI(GeoLocationRepository):
    """Implements GeoLocation web-api"""
    def __init__(self, config: Dict):
        super().__init__(config=config)
        # TODO validate config
        self.server_url = config['server_url']
        # TODO validation of exitance of the server
        # TODO whether the server is reachable (pin the server, whether the endpoint exists?)

    def geolocation_from_postal_address(self, postal_address: PostalAddress) -> GeoLocation:
        """Post request to the given server address"""
        if ~isinstance(postal_address, PostalAddress):
            warnings.warn(f"Received type: {type(postal_address)} instead of type: PostalAddress")
            return GeoLocation(0., 0.)

        message = asdict(postal_address)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(self.server_url, data=json.dumps(message), headers=headers)

        if response.status_code == 200:
            return GeoLocation({key: float(value) for key, value in response.json()})
        elif response.status_code == 400:
            warnings.warn("Request could not be parsed")
            return GeoLocation(0., 0.)
        else:
            warnings.warn(f"Server response: {response}")
            return GeoLocation(0., 0.)
