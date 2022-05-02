"""
Author: arcsi1989
"""
from abc import ABC
from typing import Dict, List

from src.common.types import PostalAddress


class PostalAddressRepository(ABC):
    """
    Implements an abstract postal-address repository functioning as an interface
    """
    def __init__(self, config: Dict):
        self.config = config
        self._repository: List[PostalAddress] = list()

    @property
    def repository(self):
        """The complete repository of the postal addresses as a list of postal addresses """
        return self._repository
