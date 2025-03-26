import pandas as pd
import numpy as np
import logging

from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class EfficiencyStrategy(ABC):
    """Abstract base class for different efficiency calculation strategies."""

    @abstractmethod
    def calculate(self, df:pd.DataFrame) -> pd.DataFrame:
        pass

class BasicEfficiencyStrategy(EfficiencyStrategy):
    """Basic efficiency calculation strategy."""
    def calculate(self, df):
        logging.info('Applying Basic Efficiency Strategy')
        # df['utilizationRate'] = df.usedInventory / df.totalInventory
        # df['idleInventoryRatio'] = (df.totalInventory - df.usedInventory) / df.totalInventory
        df["utilizationRate"] = df["quantityAvailable"] / df["quantityAvailable"].sum()
        df["idleInventoryRatio"] = 1 - df["utilizationRate"]
        return df
    
class AdvancedEfficiencyStrategy(EfficiencyStrategy):
    """Advanced efficiency calculation using weighted utilization and variance."""
    def calculate(self, df):
        logging.info("Applying Advanced Efficiency Strategy")
        df['weightedUtilization'] = np.where(df.priorityLevel > 1, df.usedInventory * 1.2, df.usedInventory)
        df['variance'] = df.usedInventory.rolling(window=5).std()
        df.fillna(0, inplace=True)
        return df
    
class OptimizationEfficiencyStrategy(EfficiencyStrategy):
    """Optimization-based efficiency calculation using linear programming."""

    def calculate(self, df):
        from scipy.optimize import linprog
        logging.info("Applying Optimization-Based Efficiency Strategy")
        c = -df.usedInventory.values
        A_eq = [df.totalInventory.values]
        b_eq = [df.availableCapacity.sum()]

        result = linprog(c, A_eq=A_eq, b_eq=b_eq, methods='highs')
        df['OptimizationUtilization'] = result.x if result.success else df.usedInventory
        return df
