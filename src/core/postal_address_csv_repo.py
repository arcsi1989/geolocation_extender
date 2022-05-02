"""
Author: arcsi1989
"""

from typing import Dict, Tuple
import pandas as pd
from csv import reader
import multiprocessing as mp

from src.interfaces.postal_address_repository import PostalAddressRepository
from src.common.types import PostalAddress


def create_postal_address(data_tuple: Tuple) -> PostalAddress:
    """Creates a postal address from data tuple"""
    if len(data_tuple) == 4:
        raise ValueError(f"Address information is not complete")
    # TODO validate received tuples values

    return PostalAddress(street_number=data_tuple[0],
                         street=data_tuple[1],
                         zip=data_tuple[2],
                         locality=data_tuple[3])


class PostalAddressCSVRepository(PostalAddressRepository):
    """Implements a Postal Address Repository created from 'die Post' csv datasource"""
    def __init__(self, config: Dict):
        super().__init__(config=config)
        # TODO sanity check whether exist config parts exists and valid
        self.filename = self.config['file']
        self.encoding = self.config['encoding']
        self.tables = self.config['tables']
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

        tables_with_requested_data = list(self.tables.keys())
        extracted_data = {table: list() for table in tables_with_requested_data}

        # Load and extract addresses from CSV file
        print('Log: CSV loading has been started')
        with open(self.filename, 'r', encoding=self.encoding) as read_obj:
            # Pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                row_values = row[0].split(';')
                # table is the ID of the original tables of database
                table = row_values[0]

                if table in tables_with_requested_data:
                    extracted_data[table].append([row_values[i] for i in list(self.tables[table].values())])

        print('Log: CSV loading has been finished')
        # Create Postal addresses
        # Create data tables
        print('Log: Creating data tables has been started')
        data_tables = dict()
        for table in tables_with_requested_data:
            data_tables[table] = pd.DataFrame(data=extracted_data[table],
                                              columns=list(self.tables[table].keys()))
        # Fuse data_tables
        # TODO resolve iterative
        f1 = pd.merge(data_tables["06"], data_tables["04"], how='inner', on='STRID')
        # print(f1.shape)
        final_table = pd.merge(f1, data_tables["01"], on='ONRP')

        if False:
            print('Log: Fusing data tables has been started')
            fused_tables = {'joined_tables': set(), 'table' : None}
            for key, tables in self.linking_keys.items():
                if len(tables) == 2:
                    if fused_tables['joined_tables'].intersection(set(tables)):
                        # TODO mechanism identify linking tables
                        fused_tables['joined_tables'] = fused_tables['joined_tables'].union(set(tables))
                        fused_tables['table'] = pd.merge(left=fused_tables['table'],
                                                         right=data_tables[tables[1]],
                                                         how='inner', on=key)
                    else:
                        fused_tables['joined_tables'] = set(tables)
                        fused_tables['table'] = pd.merge(left=data_tables[tables[0]],
                                                         right=data_tables[tables[1]],
                                                         how='inner', on=key)
                else:
                    if len(tables) <= 1:
                        raise ValueError(f"Only 1 or none table assigned to the linking key")
                    else:
                        raise NotImplementedError(f"Method to join more than two tables is not implement")
            # TODO multilayer fusion of the data tables
            final_table = fused_tables['table']

        # TODO parallelization of registry creating
        print('Log: Creating repository')
        #print(final_table.shape)
        #print(final_table.columns)
        df = final_table[['HNR', 'STR_BEZ_K', 'PLZ', 'ORT_BEZ_18']]

        # Create repository - list of postal addresses"""
        num_cores = mp.cpu_count()
        with mp.Pool(num_cores - 1) as pool:
            result = pool.imap(create_postal_address, df.itertuples(name=None), chunksize=1000)
            self._repository = [x for x in result]
