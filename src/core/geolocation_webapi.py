"""
Author: arcsi1989
"""
from typing import Dict
import warnings

import requests
import json
from dataclasses import asdict

from src.interfaces.geolocation_repository import GeoLocationRepository
from src.common.types import PostalAddress, GeoLocation


class GeoLocationWebAPI(GeoLocationRepository):
    """
    Implements GeoLocation WebAPI configured by a single address
    The config file constains only:
        server_url (str): location of the WebAPI
    """

    def __init__(self, config: Dict):
        super().__init__(config=config)
        # TODO validate config
        # TODO validation of existance of the server
        # TODO whether the server is reachable (pin the server, whether the endpoint exists?)
        self.server_url = config['server_url']

    def geolocation_from_postal_address(self, postal_address: PostalAddress) -> GeoLocation:
        """
        Post request to the given server address
        If the received answer is the corresponding GeoLocation is returned, otherwise a GeoLocation with (0,0)
        coordinates
        """
        if isinstance(postal_address, PostalAddress):
            message = {key: str(value) for key, value in asdict(postal_address).items()}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = requests.post(self.server_url, data=json.dumps(message), headers=headers)

            if response.status_code == 200:
                return GeoLocation(**{key: float(value) for key, value in response.json()})
            elif response.status_code == 400:
                warnings.warn("Request could not be parsed")
                return GeoLocation(0., 0.)
            else:
                warnings.warn(f"Server response: {response}")
                return GeoLocation(0., 0.)
        else:
            warnings.warn(f"Received type: {type(postal_address)} instead of type: PostalAddress")
            return GeoLocation(0., 0.)
