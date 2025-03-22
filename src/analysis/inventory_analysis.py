import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

import numpy as np
import pandas as pd

from data_ingestion.csv_loader import CSVLoader
from efficiency_strategies import EfficiencyStrategy

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class InventoryAnalysis:
    """
    Class to analyze inventory efficiency using different strategies.
    Supports asyncio for async operations, multithreading for I/O, and multiprocessing for computation.
    """

    def __init__(self, strategy: EfficiencyStrategy):
        self._strategy = strategy
        self.csv_loader = CSVLoader()

    async def load_data(self, file_path: str) -> pd.DataFrame:
        """Asynchronously load data using pandas or polars."""
        logging.info(f"Loading data from {file_path}")
        loop = asyncio.get_event_loop()
        df = await loop.run_in_executor(None, self.csv_loader.load_with_pandas, file_path)
        return df

    def compute_metrics(self, df: pd.DataFrame):
        """Compute inventory efficiency metrics."""
        logging.info("Computing efficiency metrics...")
        return self._strategy.calculate(df)

    def parallel_compute(self, df: pd.DataFrame):
        """Parallel computation using multiprocessing."""
        logging.info("Starting parallel computation")
        num_partitions = cpu_count()
        df_split = np.array_split(df, num_partitions)

        with ProcessPoolExecutor(max_workers=num_partitions) as executor:
            results = list(executor.map(self.compute_metrics, df_split))

        return pd.concat(results)

    async def run_analysis(self, inventory_file: str):
        """Run the full inventory efficiency analysis asynchronously."""
        df = await self.load_data(inventory_file)

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.parallel_compute, df)
        logging.info("Analysis complete")
        return result


# Example Usage
if __name__ == '__main__':
    from efficiency_strategies import BasicEfficiencyStrategy

    strategy = BasicEfficiencyStrategy()
    analysis = InventoryAnalysis(strategy)

    asyncio.run(analysis.run_analysis('data/inventory_data.csv'))