"""
Author: arcsi1989
Definition of dataclasses used to manage program specific data types.
"""

from dataclasses import dataclass


@dataclass
class PostalAddress:
    """Postal Address"""
    street: str
    street_number: int
    zip: int
    locality: str


@dataclass
class GeoLocation:
    """Geo Location"""
    latitude: float
    longitude: float
