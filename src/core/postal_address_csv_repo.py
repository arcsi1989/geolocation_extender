"""
Author: arcsi1989
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np
import multiprocessing as mp

from src.interfaces.postal_address_repository import PostalAddressRepository
from src.common.types import PostalAddress
from src.utils.preprocess_tables import parse_tables


def create_postal_address(data_tuple: Tuple) -> PostalAddress:
    """
    Creates a postal address from data tuple
    Example data tuple:
        data_tuple[0]: row number in data_frame - ignore
        data_tuple[1]: street number
        data_tuple[2]: street
        data_tuple[3]: zip code
        data_tuple[4]: locality
    """
    if len(data_tuple) != 5:
        raise ValueError(f"Address information is not complete")
    # Street number
    if np.isnan(data_tuple[1]):
        street_number = ""
    else:
        street_number = int(data_tuple[1])

    return PostalAddress(street_number=street_number,
                         street=data_tuple[2],
                         zip=data_tuple[3],
                         locality=data_tuple[4])


class PostalAddressCSVRepository(PostalAddressRepository):
    """Implements a Postal Address Repository created from 'die Post' csv datasource"""

    def __init__(self, config: Dict):
        super().__init__(config=config)
        # TODO sanity check whether exist config parts exists and valid
        self.file_path = self.config['file_path']
        self.csv_file = self.config['csv_file']
        self.encoding = self.config['encoding']
        self.tables_config = self.config['tables']
        self.tables = None
        self.linking_keys = self.config['linking_keys']
        self.postal_address_attributes = self.config['postal_address']
        self._load_csv_file()
        self._num_address = None

    @property
    def num_address(self):
        """Number of addresses in the repository"""
        return self._num_address

    def _load_csv_file(self):
        """Loads the addresses into the repository from a csv file"""

        # Loading postal addresses
        self.tables = parse_tables(file_path=self.file_path, csv_file=self.csv_file,
                                   encoding=self.encoding, tables_config=self.tables_config)

        # Fusing data tables
        print('Log: Fusing data tables has been started')
        fused_tables = None
        for key, tables in self.linking_keys.items():
            if len(tables) == 2:
                if fused_tables is None:
                    fused_tables = pd.merge(left=self.tables[tables[0]],
                                            right=self.tables[tables[1]],
                                            how='inner', on=key)
            elif len(tables) == 1:
                fused_tables = pd.merge(left=fused_tables,
                                        right=self.tables[tables[0]],
                                        how='inner', on=key)
            else:
                raise NotImplementedError(f"Method to join more than two tables is not implement")

        print('Log: Start to create postal addresses')
        df = fused_tables[['HNR', 'STRBEZK', 'POSTCODE', 'ORTBEZ18']]
        # Create repository - list of postal addresses"""
        num_cores = mp.cpu_count()
        with mp.Pool(num_cores - 1) as pool:
            result = pool.imap(create_postal_address, df.itertuples(name=None), chunksize=1000)
            self._repository = [x for x in result]

        print('Log: Finished creating postal addresses')
