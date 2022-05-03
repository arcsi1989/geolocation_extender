import os
from pathlib import Path
import os.path
from typing import Dict
import pandas as pd
import time


def parse_tables(file_path: str, csv_file: str, encoding: str, tables_config: Dict) -> Dict:
    print('Log: CSV loading has been started')
    bash_folder = str(Path(__file__).parent)
    os.system(f"source {bash_folder}/slice_tables.sh {file_path} {csv_file}")
    latest_file = file_path + "/08.csv"
    if os.path.isfile(latest_file):
        print("Successful data splitting")
    else:
        raise ValueError("File split is failed")

    tables = dict()
    for idx, key in enumerate(tables_config.keys()):
        table_file = f"{file_path}/0{idx}.csv"
        if os.path.isfile(table_file):
            tables[key] = pd.read_csv(table_file, sep=';', header=None, encoding=encoding)
            tables[key].columns = list(tables_config[key]['fields'].keys())
            # tables[key].astype(tables_config[key]['fields'])

    print('Log: CSV loading has been finished')

    return tables
