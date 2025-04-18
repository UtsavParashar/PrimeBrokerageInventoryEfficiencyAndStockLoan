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

    def _random_date(self, start: str='2024-01-01', end: str='2025-03-20', sort: bool = False) -> np.ndarray:
        """Generate random dates within a given range."""
        date_series = pd.Series(np.random.choice(pd.date_range(start, end), size=self.num_rows))
        date_series = date_series.sort_values() if sort else date_series
        return date_series.dt.date.astype(str)

    def generate_inventory_data(self) -> None:
        """Generate inventory data and save as CSV."""
        inventory_data = pd.DataFrame({
            'tradeDate': self._random_date(sort=True),
            'securityId': np.random.choice([f'SEC-{i}' for i in range(1000, 1021)], self.num_rows),
            'quantityAvailable': np.random.randint(100, 1000, self.num_rows),
            'marketPrice': np.round(np.random.uniform(10, 500, self.num_rows), 2),
            'region': np.random.choice(['EMEA', 'APAC', 'US'], self.num_rows)
        })
        inventory_data.insert(2, 'securityName', 'Stock-' + inventory_data.securityId.str.split('-').str[-1])
        CSVGenerator.store_csv(inventory_data, 'inventory_data.csv')

    def generate_stock_loan_data(self) -> None:
        stock_loan_data = pd.DataFrame({
            "loanDate": self._random_date(sort=True),
            "securityId": np.random.choice([f"SEC-{i}" for i in range(1000, 1021)], self.num_rows),
            "counterpartyId": np.random.choice([f"CP-{i}" for i in range(1, 10)], self.num_rows),
            "quantityBorrowed": np.random.randint(10, 5000, self.num_rows),
            "quantityReturned": np.random.randint(0, 5000, self.num_rows),
            "loanFee": np.round(np.random.uniform(0.1, 5.0, self.num_rows), 2),
            "borrowFee": np.round(np.random.uniform(0.1, 5.0, self.num_rows), 2),
            "rebateRate": np.round(np.random.uniform(0.1, 2.0, self.num_rows), 2),
        })
        CSVGenerator.store_csv(stock_loan_data, 'stock_loan_data.csv')

    def generate_all(self):
        """Generate all the csvs """
        self.generate_inventory_data()
        self.generate_stock_loan_data()

    @staticmethod
    def store_csv(df: pd.DataFrame, file: str, path: str = None) -> None:
        """Store DataFrame as a CSV file."""
        if path is None:
            path = Path(__file__).parent / './../../data'
        os.makedirs(path, exist_ok=True)
        logging.info(f'Storing csv for {file}')
        try:
            df.to_csv(os.path.join(path, file), index=False)
        except:
            logging.error('Error storing csv - {file}')
            raise


if __name__ == '__main__':
    CSVGenerator().generate_all()
