import pandas as pd
import numpy as np
import logging

from abc import ABC, abstractmethod
from scipy.optimize import linprog

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
        grouped = df.groupby("securityId")
        df["utilizationRate"] = grouped["quantityAvailable"].transform(lambda x: x / x.sum())
        df["idleInventoryRatio"] = 1 - df["utilizationRate"]
        return df
    
class AdvancedEfficiencyStrategy(EfficiencyStrategy):
    """Advanced efficiency calculation using weighted utilization and variance."""
    def calculate(self, df):
        logging.info("Applying Advanced Efficiency Strategy")
        # df['weightedUtilization'] = np.where(df.priorityLevel > 1, df.usedInventory * 1.2, df.usedInventory)
        # df['variance'] = df.usedInventory.rolling(window=5).std()
        df['weightedUtilization'] = np.where(df["marketPrice"] > df.groupby("securityId")["marketPrice"].transform("median"), df["quantityAvailable"] * 1.2, df["quantityAvailable"])
        df["variance"] = df.groupby("securityId")["quantityAvailable"].transform(lambda x: x.rolling(window=5, min_periods=1).std())
        df.fillna(0, inplace=True)
        return df
    
class OptimizationEfficiencyStrategy(EfficiencyStrategy):
    """Optimization-based efficiency calculation using linear programming."""

    def calculate(self, df):
        def optimize_inventory(group):
            c = -group["quantityAvailable"].values  # Maximization problem
            A_eq = [group["quantityAvailable"].values]
            b_eq = [group["quantityAvailable"].sum()]
            
            result = linprog(c, A_eq=A_eq, b_eq=b_eq, method="highs")
            
            group["optimizedUtilization"] = result.x if result.success else group["quantityAvailable"]
            
            # Calculate utilizationRate and idleInventoryRatio based on optimized utilization
            group["utilizationRate"] = group["optimizedUtilization"] / group["optimizedUtilization"].sum()
            group["idleInventoryRatio"] = 1 - group["utilizationRate"]
            
            return group
        
        df = df.groupby("securityId", group_keys=False).apply(optimize_inventory)
        return df
