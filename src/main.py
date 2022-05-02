"""
Author: arcsi1989
"""
from pathlib import Path
import json

from src.core import PostalAddressCSVRepository, GeoLocationWebAPI, PostalAddressGeoEnricher, GeoLocationWebAPIDummy


def address_enriching_program():
    # Load program specific config file
    with open((Path(__file__).parents[1] / "config/program_config.json").resolve(), "rb") as file:
        config = json.load(file)

    # Create PostalAddressCSVRepository
    repository = PostalAddressCSVRepository(config=config["address_repository"])

    # Create GeoLocation Repository
    if config['geolocation_repository']['server_url']:
        geo_loc_webapi = GeoLocationWebAPI(config=config['geolocation_repository'])
    else:
        geo_loc_webapi = GeoLocationWebAPIDummy(config=config['geolocation_repository'])

    # Create GeoLocation enricher for postal addresses
    postal_address_geo_enricher = PostalAddressGeoEnricher(geo_repo=geo_loc_webapi)

    # Enrich postal addresses with geolocation
    postal_address_geo_enricher.enrich_addresses(repository.repository)

    # Dump enriched addresses to defined output json file
    final_file = {"type": "FeatureCollection", "features": postal_address_geo_enricher.geo_json_addresses}
    with open(config['output_file'],  "w") as f:
        json.dump(final_file, f)


if __name__ == '__main__':
    address_enriching_program()
