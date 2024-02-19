import pandas as pd
import talib


class TradingIndicators:
    def __init__(self, df):
        self.df = df

    def calculate_rsi(self, period):
        self.df[f'rsi_{period}'] = talib.RSI(self.df['close'], timeperiod=period)
        return self.df

    def calculate_macd(self, period_long, period_short, period_signal):
        self.df['macd'], self.df['signal'], self.df['hist'] = talib.MACD(self.df['close'], fastperiod=period_short, slowperiod=period_long, signalperiod=period_signal)
        return self.df

    def calculate_bollinger_bands(self, period):
        self.df[f'upper_band_{period}'], self.df[f'middle_band_{period}'], self.df[f'lower_band_{period}'] = talib.BBANDS(self.df['close'], timeperiod=period)
        return self.df

    def calculate_atr(self, period):
        self.df[f'atr_{period}'] = talib.ATR(self.df['high'], self.df['low'], self.df['close'], timeperiod=period)
        return self.df

    def calculate_obv(self):
        self.df['obv'] = talib.OBV(self.df['close'], self.df['volume'])
        return self.df

    def calculate_ema(self, period):
        self.df[f'ema_{period}'] = talib.EMA(self.df['close'], timeperiod=period)
        return self.df

    def calculate_sma(self, period):
        self.df[f'sma_{period}'] = talib.SMA(self.df['close'], timeperiod=period)
        return self.df


