"""
Author: arcsi1989
"""
from abc import ABC
from typing import Dict, List

from common.types import PostalAddress


class PostalAddressRepository(ABC):
    def __init__(self, config: Dict):
        self.config = config
        self._repository: List[PostalAddress] = list()

    @property
    def repository(self):
        return self._repository
