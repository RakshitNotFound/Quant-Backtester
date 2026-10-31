# Quant Backtester & Execution Simulation Engine

A Python-based quantitative backtesting and execution framework designed to simulate market microstructure dynamics, performance metrics, and risk-managed trading strategies.

## 🚀 Features
* **Historical Data Ingestion:** Seamlessly pulls and parses historical price and volume data using `yfinance`.
* **Technical Analysis Integration:** Incorporates technical indicator calculations via the `ta` library to generate rule-based trading signals.
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
```

---

## ⚙️ Installation & Setup

```bash
git clone [https://github.com/RakshitNotFound/quant-backtester.git](https://github.com/RakshitNotFound/quant-backtester.git)
cd quant-backtester
python -m venv venv
venv\Scripts\activate
pip install numpy pandas matplotlib ta yfinance
```

---

## 📊 Running the Backtest

Execute the script directly from your terminal or IDE:
```bash
python backtest.py
```

### Sample Output Metrics
```text
--- Performance Metrics ---
Initial Capital: $1,000,000.00
Final Portfolio Value: $1,006,081.19
Total Returns: 0.61%
Annualized Returns: 0.10%
Volatility: 0.45%
Sharpe Ratio: -4.17
Total P&L: $-2,636.43
Average Trade Return: -0.07%
Win Ratio: 50.00%
```

---

## 🔬 Future Enhancements
* Transitioning from a vectorized approach to a full **Event-Driven Architecture** (using priority event queues for Market, Signal, Order, and Fill events).
* Implementing advanced slippage and market impact models (e.g., square-root law).
* Expanding strategy modules to include statistical arbitrage (Pairs Trading / Ornstein-Uhlenbeck mean-reversion processes).

---

## 👤 Author
**Rakshit (Rune)**  
*Full-Stack & Systems Software Engineer | Quantitative Development Enthusiast*
