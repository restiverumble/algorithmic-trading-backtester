# Vectorized Algorithmic Trading Backtester

This is an algorithmic trading backtester that uses high-performance Python code for historical simulations of financial assets. The backtester takes advantage of Pandas vectorization, enabling fast strategy evaluation without iterative looping and calculation of performance metrics at the institutional level.

## Tech Stack
* **Language:** Python
* **Data Processing & Vectorization:** Pandas, NumPy
* **Market Data:** yfinance

## Core Features & Methodology
* **Vectorized Execution Pipeline:** Strategy logic and portfolio compounding are performed through Pandas vectorization for efficient processing of historical data and faster iterations.
* **Automated Data Acquisition:** Built-in functionality for fetching historical pricing data from the Yahoo Finance API.
* **Performance Metrics:** Automatic performance evaluation of the strategy relative to its capital using standard industry metrics:
  * **Compound Annual Growth Rate (CAGR):** Measures the mean annual growth rate of the portfolio.
  * **Maximum Drawdown (MDD):** Determines the maximum decline in the portfolio’s value to evaluate historical risk exposure.
  * **Sharpe Ratio:** Assesses risk-adjusted returns based on the annualised ratio of the excess return to standard deviation.
## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/restiverumble/algorithmic-trading-backtester.git
   cd algorithmic-trading-backtester
2. **Install dependencies:**
    ```bash
   pip install -r requirements.txt
3. **Run the backtester:**
    ```bash
   python -m engine.backtester
