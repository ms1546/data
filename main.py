import yfinance as yf
import matplotlib.pyplot as plt

# fetchdata
ticker = "AAPL"  # Apple Inc
data = yf.download(ticker, start="2023-01-01", end="2024-01-01")

# 移動平均の計算
short_window = 30
long_window = 100

# 短期間移動平均
data['30_day_MA'] = data['Close'].rolling(window=short_window).mean()

# 長期間移動平均
data['100_day_MA'] = data['Close'].rolling(window=long_window).mean()

# ボラティリティ
data['Daily_Return'] = data['Close'].pct_change()
data['Volatility'] = data['Daily_Return'].rolling(window=30).std()

# 株価と移動平均のプロット
plt.figure(figsize=(14,7))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['30_day_MA'], label='30-Day Moving Average')
plt.plot(data['100_day_MA'], label='100-Day Moving Average')
plt.title('Stock Price and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# ボラティリティのプロット
plt.figure(figsize=(14,7))
plt.plot(data['Volatility'], label='Rolling Volatility (30-day)')
plt.title('Stock Price Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()
plt.show()
