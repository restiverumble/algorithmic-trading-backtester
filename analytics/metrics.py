import numpy as np
import pandas as pd

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0, trading_days: int = 252) -> float:
    """
    Calculates the annualised Sharpe Ratio
    """
    # daily excess returns
    excess_returns = returns - (risk_free_rate / trading_days)
    
    if excess_returns.std() == 0:
        return 0.0
        
    # annualise
    sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(trading_days)
    return round(sharpe, 2)

def calculate_max_drawdown(portfolio_values: pd.Series) -> float:
    """
    Calculates the Maximum Drawdown 
    """
    # running max
    rolling_max = portfolio_values.cummax()
    
    # % drop from peak
    drawdown = (portfolio_values / rolling_max) - 1.0
    
    return round(drawdown.min(), 4)

def calculate_cagr(portfolio_values: pd.Series, trading_days: int = 252) -> float:
    """
    Calculates the Compound Annual Growth Rate
    """
    if len(portfolio_values) < 2:
        return 0.0
        
    start_value = portfolio_values.iloc[0]
    end_value = portfolio_values.iloc[-1]
    
    # total years
    years = len(portfolio_values) / trading_days
    
    cagr = (end_value / start_value) ** (1 / years) - 1
    return round(cagr, 4)

def generate_performance_report(df: pd.DataFrame) -> dict:
    """
    Generates a performance report for a given DataFrame
    """
    strategy_returns = df['net_strategy_return']
    portfolio_values = df['portfolio_value']
    
    return {
        "Total Return (%)": round((portfolio_values.iloc[-1] / portfolio_values.iloc[0] - 1) * 100, 2),
        "CAGR (%)": round(calculate_cagr(portfolio_values) * 100, 2),
        "Max Drawdown (%)": round(calculate_max_drawdown(portfolio_values) * 100, 2),
        "Sharpe Ratio": calculate_sharpe_ratio(strategy_returns)
    }