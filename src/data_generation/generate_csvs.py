import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CSVGenerator:
    """Class to generate inventory and stock load data in CSV format."""

    def __init__(self, num_rows: int = 100) -> None:
        self.num_rows = num_rows

    def _random_date(self, start: str, end: str) -> np.ndarray:
        """Generate random dates within a given range."""
        return np.random.choice(pd.date_range(start, end), size=self.num_rows)

    def generate_inventory_data(self) -> None:
        """Generate inventory data and save as CSV."""
        inventory_data = pd.DataFrame({
            'tradeDate': pd.Series(self._random_date('2024-01-01', '2025-03-20')).dt.date.astype(str),
            'securityId': np.random.choice([f'SEC-{i}' for i in range(1000, 1021)], self.num_rows),
            'quantityAvailable': np.random.randint(100, 1000, self.num_rows),
            'marketPrice': np.round(np.random.uniform(10, 500, self.num_rows), 2),
            'region': np.random.choice(['EMEA', 'APAC', 'US'], self.num_rows)
        })
        inventory_data.insert(2, 'securityName', 'Stock-' + inventory_data.securityId.str.split('-').str[-1])
        CSVGenerator.store_csv(inventory_data, 'inventory_data.csv')

    @staticmethod
    def store_csv(df: pd.DataFrame, file: str, path: str = None) -> None:
        """Store DataFrame as a CSV file."""
        if path is None:
            path = Path(__file__).parent / './../../data'
        os.makedirs(path, exist_ok=True)
        df.to_csv(os.path.join(path, file), index=False)


if __name__ == '__main__':
    CSVGenerator().generate_inventory_data()
