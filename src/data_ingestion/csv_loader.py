import pandas as pd
import numpy as np
import polars as pl
import dask.dataframe as dd
import scipy as stats

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CSVLoader:
    """Class to load and process CSV data using Pandas, Polars, or Dask."""

    def __init__(self, file_path):
        self.file_path = file_path

    def _normalize_columns(self, column):
        """Normalize numeric column values using Min-Max Scaling"""
        return (column - np.min(column))/np.max(column) - np.min(column)
    
    def load_with_pandas(self):
        """Load CSV using Pandas with logging and error handling."""
        
        logging.info(f'Loading {self.file_path} with pandas')
        try:
            df = pd.read_csv(self.file_path)
        except Exception as e:
            logging.error(f"Error loading {self.file_path} using Pandas: {e}")
            raise e
        
        # First column is expected to be of date type
        try:
            df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
        except Exception as e:
            logging.error(f"Error converting {df.columns[0]} to datetime: {e}")
            raise e
        
        # Normalize numeric columns
        # numeric_cols = df.select_dtypes(include=[np.number]).columns
        # df[numeric_cols] = df[numeric_cols].apply(self._normalize_columns)
        
        logging.info(f"Loaded {self.file_path} with {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    
if __name__ == '__main__':
    inventory_loader = CSVLoader('data/inventory_data.csv')
    stock_loan_loader = CSVLoader("data/stock_loan_data.csv")
    inventory_loader_df = inventory_loader.load_with_pandas()
    stock_loan_df = stock_loan_loader.load_with_pandas()
    print(inventory_loader_df.head())
    print(stock_loan_df.head())
        