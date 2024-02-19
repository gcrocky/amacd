import matplotlib.pyplot as plt

class TradingStrategy:
    def __init__(self, df):
        self.df = df

    def find_cross_points(self):
        cross_points = (self.df['macd'].shift(1) < self.df['signal'].shift(1)) & (self.df['macd'] > self.df['signal']) & (self.df['macd'] < -500)
        return cross_points

