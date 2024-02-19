import pandas as pd

class TradingIndicators:
    def __init__(self, df):
        self.df = df

    def calculate_sma(self, period):
        self.df[f'sma_{period}'] = self.df['close'].rolling(window=period).mean()
        return self.df

    def calculate_ema(self, period):
        self.df[f'ema_{period}'] = self.df['close'].ewm(span=period, adjust=False).mean()
        return self.df
