import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np

def analyze_stock_data(data):
    short_window = 30
    long_window = 100

    data['30_day_MA'] = data['Close'].rolling(window=short_window).mean()
    data['100_day_MA'] = data['Close'].rolling(window=long_window).mean()
    data['Daily_Return'] = data['Close'].pct_change()
    data['Volatility'] = data['Daily_Return'].rolling(window=30).std()

    return data

class TestStockAnalysis(unittest.TestCase):

    @patch('yfinance.download')
    def test_analyze_stock_data(self, mock_download):
        # モックデータ
        np.random.seed(0)
        prices = [100]  # 初期株価
        for _ in range(1, 120):
            change = 1 + np.random.uniform(-0.01, 0.01)
            prices.append(prices[-1] * change)

        mock_data = pd.DataFrame({'Close': prices})
        mock_download.return_value = mock_data


        # テスト実行
        result = analyze_stock_data(mock_download('AAPL', '2023-01-01', '2024-01-01'))

        # アサーション
        self.assertIsNotNone(result)
        self.assertFalse(result.empty)
        self.assertIn('30_day_MA', result)
        self.assertIn('100_day_MA', result)
        self.assertIn('Daily_Return', result)
        self.assertIn('Volatility', result)

        # 移動平均のテスト
        self.assertTrue(np.all(np.isclose(result['30_day_MA'].iloc[29:],
                                          result['Close'].rolling(window=30).mean().iloc[29:])))
        self.assertTrue(np.all(np.isclose(result['100_day_MA'].iloc[99:],
                                          result['Close'].rolling(window=100).mean().iloc[99:])))

        # ボラティリティのテスト
        expected_volatility = result['Daily_Return'].rolling(window=30).std().iloc[29:]
        calculated_volatility = result['Volatility'].iloc[29:]
        for i, (expected, calculated) in enumerate(zip(expected_volatility, calculated_volatility)):
            if np.isnan(expected) and np.isnan(calculated):
                continue  # 両方がnanの場合
            self.assertTrue(np.isclose(expected, calculated, atol=1e-6), f"At index {i}: expected {expected}, got {calculated}")

if __name__ == '__main__':
    unittest.main()
