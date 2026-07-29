import numpy as np
import pandas as pd
from data.data_loader import fetch_historical_data
from analytics.metrics import generate_performance_report

class VectorizedBacktester:
    """
    Vectorized engine for simulating trading strategies.
    Accounts for look-ahead bias and transaction frictions.
    """
    def __init__(
        self,
        df: pd.DataFrame,
        initial_capital: float = 10000.0,
        commission: float = 0.001,  # 0.1% per trade
        slippage: float = 0.0005    # 0.05% per trade
    ):
        self.df = df.copy()
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.total_friction = self.commission + self.slippage

    def run_moving_average_crossover(self, short_window: int = 20, long_window: int = 50) -> pd.DataFrame:
        """
        Moving Average Crossover strategy.
        Goes long (1) when short SMA > long SMA, otherwise holds cash (0).
        """
        # Moving averages
        self.df['sma_short'] = self.df['close'].rolling(window=short_window).mean()
        self.df['sma_long'] = self.df['close'].rolling(window=long_window).mean()

        # Signal generation (1 = Long, 0 = Cash)
        self.df['raw_signal'] = np.where(self.df['sma_short'] > self.df['sma_long'], 1, 0)

        # Shift signals by 1 period to prevent look-ahead bias
        self.df['position'] = self.df['raw_signal'].shift(1)

        # Identify trade execution days
        self.df['trade_executed'] = self.df['position'].diff().fillna(0).abs()

        # Return calculations
        self.df['gross_strategy_return'] = self.df['position'] * self.df['daily_return']
        self.df['friction_penalty'] = self.df['trade_executed'] * self.total_friction
        self.df['net_strategy_return'] = self.df['gross_strategy_return'] - self.df['friction_penalty']

        # Cumulative equity curve
        self.df['cum_market_return'] = (1 + self.df['daily_return']).cumprod()
        self.df['cum_strategy_return'] = (1 + self.df['net_strategy_return']).cumprod()

        self.df['portfolio_value'] = self.initial_capital * self.df['cum_strategy_return']

        # Drop warm-up period NaNs
        self.df = self.df.dropna()

        return self.df


if __name__ == "__main__":
    # Test the backtester engine
    data = fetch_historical_data("AAPL", "2020-01-01", "2024-01-01")
    
    backtester = VectorizedBacktester(
        df=data,
        initial_capital=10000.0,
        commission=0.001,  
        slippage=0.0005     
    )
    
    results = backtester.run_moving_average_crossover(short_window=20, long_window=50)
    
    print("\nBacktest Execution Complete!")
    print(results[['close', 'sma_short', 'sma_long', 'position', 'trade_executed', 'net_strategy_return', 'portfolio_value']].tail())

    report = generate_performance_report(results)
    print("\n--- Strategy Performance Report ---")
    for key, value in report.items():
        print(f"{key}: {value}")