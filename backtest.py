import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ta
import yfinance as yf


def load_market_data(symbol, start_date, end_date):
  data = yf.download(symbol, start=start_date, end=end_date)
  if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
  return data


class BacktestingEngine:

  def __init__(self, data, initial_capital=1000000.0, risk_per_trade=0.02):
    self.data = data.copy()
    self.initial_capital = initial_capital
    self.risk_per_trade = risk_per_trade
    self.portfolio_values = []
    self.trades = []

  def run_backtest(self):
    cash = self.initial_capital
    position = 0.0  # shares held
    portfolio_history = []

    # Shift signal by 1 to prevent look-ahead bias
    self.data['Executed_Signal'] = self.data['signal'].shift(1).fillna(0)

    for i, (date, row) in enumerate(self.data.iterrows()):
      close_price = row['Close']
      signal = row['Executed_Signal']

      # Track portfolio value at the start of the day
      current_portfolio_value = cash + (position * close_price)
      portfolio_history.append(
          {'Date': date, 'Portfolio_Value': current_portfolio_value}
      )

      # Buy Signal (Enter long only if flat)
      if signal == 1 and position == 0:
        capital_to_risk = cash * self.risk_per_trade
        position = capital_to_risk / close_price
        cash -= position * close_price
        self.trades.append(
            {'Date': date, 'Type': 'BUY', 'Price': close_price, 'Shares': position}
        )

      # Sell Signal (Exit long only if holding position)
      elif signal == -1 and position > 0:
        cash += position * close_price
        self.trades.append(
            {'Date': date, 'Type': 'SELL', 'Price': close_price, 'Shares': position}
        )
        position = 0.0

    self.data['Portfolio_Value'] = [p['Portfolio_Value'] for p in portfolio_history]
    self.data['Returns'] = self.data['Portfolio_Value'].pct_change().fillna(0)

  def calculate_performance(self):
    if not self.trades:
      return 0, 0, 0

    pnl_list = []
    buy_trade = None
    for trade in self.trades:
      if trade['Type'] == 'BUY':
        buy_trade = trade
      elif trade['Type'] == 'SELL' and buy_trade is not None:
        pnl = (trade['Price'] - buy_trade['Price']) * trade['Shares']
        pnl_list.append(pnl)
        buy_trade = None

    total_pnl = sum(pnl_list) if pnl_list else 0
    win_ratio = (
        sum(1 for p in pnl_list if p > 0) / len(pnl_list) if pnl_list else 0
    )
    avg_trade_return = (
        np.mean([p / self.initial_capital for p in pnl_list]) if pnl_list else 0
    )

    return total_pnl, avg_trade_return, win_ratio

  def plot_portfolio_value(self):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(
        self.data.index,
        self.data['Portfolio_Value'],
        label='Portfolio Value',
        color='blue',
    )
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Portfolio Value ($)', color='blue')
    ax1.set_title('Backtest Portfolio Value Over Time')
    ax1.grid(True)
    fig.tight_layout()
    plt.show()


def main():
  print("Greetings! Enter the ticker for the security you'd like to explore:")
  symbol = input('Ticker (e.g., AAPL): ').strip().upper()
  start_date = input('Start Date (YYYY-MM-DD): ').strip()
  end_date = input('End Date (YYYY-MM-DD): ').strip()

  data = load_market_data(symbol, start_date, end_date)
  if data.empty:
    print('No data found for the given ticker and date range.')
    return

  # Define Strategy: Moving Average Crossover
  sma_short = ta.trend.sma_indicator(data['Close'], window=50)
  sma_long = ta.trend.sma_indicator(data['Close'], window=200)

  data['signal'] = np.where(sma_short > sma_long, 1, -1)

  engine = BacktestingEngine(data, initial_capital=1000000.0)
  engine.run_backtest()

  # Performance Metrics
  final_val = engine.data['Portfolio_Value'].iloc[-1]
  total_returns = (
      final_val - engine.initial_capital
  ) / engine.initial_capital
  days = len(data)
  annualized_returns = (1 + total_returns) ** (252 / days) - 1 if days > 0 else 0
  returns_series = engine.data['Returns']
  volatility = np.std(returns_series) * np.sqrt(252)
  sharpe_ratio = (
      (annualized_returns - 0.02) / volatility if volatility != 0 else 0
  )

  total_pnl, average_trade_return, win_ratio = engine.calculate_performance()

  print('\n--- Performance Metrics ---')
  print(f'Initial Capital: ${engine.initial_capital:,.2f}')
  print(f'Final Portfolio Value: ${final_val:,.2f}')
  print(f'Total Returns: {total_returns:.2%}')
  print(f'Annualized Returns: {annualized_returns:.2%}')
  print(f'Volatility: {volatility:.2%}')
  print(f'Sharpe Ratio: {sharpe_ratio:.2f}')
  print(f'Total P&L: ${total_pnl:,.2f}')
  print(f'Average Trade Return: {average_trade_return:.2%}')
  print(f'Win Ratio: {win_ratio:.2%}')

  engine.plot_portfolio_value()


if __name__ == '__main__':
  main()