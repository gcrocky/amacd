import matplotlib.pyplot as plt
import mplfinance as mpf

class TradingVisualizer:
    def __init__(self, df):
        self.df = df

    def plot_chart(self):
        # Create a new DataFrame which includes OHLC data for plotting in mplfinance
        ohlc_df = self.df[['open', 'high', 'low', 'close']].copy()

        # Define MACD and RSI plots
        ap0 = mpf.make_addplot(self.df['macd'], panel=1, color='b', secondary_y=True)
        ap1 = mpf.make_addplot(self.df['signal'], panel=1, color='r')
        ap2 = mpf.make_addplot(self.df['rsi_14'], panel=2, color='g')

        # Create the plot with the trading signal
        mpf.plot(ohlc_df, type='candle', style='yahoo', addplot=[ap0, ap1, ap2], volume=True, figratio=(10,8), title=f'{self.df.index[0]} to {self.df.index[-1]}', savefig='trading_signals.png')

    def plot_cross_points(self):
        cross_points = (self.df['macd'].shift(1) < self.df['signal'].shift(1)) & (self.df['macd'] > self.df['signal']) & (self.df['macd'] < -500)
        plt.figure(figsize=(12, 9))
        plt.plot(self.df.index, self.df['close'], label='Close Price')
        plt.scatter(self.df.index[cross_points], self.df['close'][cross_points], color='r', label='MACD cross points')
        plt.legend()
        plt.show()
