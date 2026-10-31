# Quant Backtester & Execution Simulation Engine

A Python-based quantitative backtesting and execution framework designed to simulate market microstructure dynamics, performance metrics, and risk-managed trading strategies.

## 🚀 Features
* **Historical Data Ingestion:** Seamlessly pulls and parses historical price and volume data using `yfinance`[cite: 2].
* **Technical Analysis Integration:** Incorporates technical indicator calculations via the `ta` library to generate rule-based trading signals[cite: 2].
* **Risk Management & Sizing:** Implements robust position sizing logic (e.g., fixed-fractional risk per trade) to simulate realistic capital allocation.
* **Performance Analytics:** Calculates core quantitative metrics from scratch, including:
  * Total & Annualized Returns
  * Volatility & Sharpe Ratio
  * Maximum Drawdown & Win/Loss Ratios
  * Total Profit & Loss (P&L)

---

## 🛠️ Project Structure

```text
quants/
│
├── venv/                 # Virtual environment (ignored in git)
├── backtest.py           # Main backtesting engine and strategy logic
└── README.md             # Project documentation
