import os
import ccxt
import pandas as pd
import time


class TradingData:
    def __init__(self, exchange_name, symbol, timeframe, filename):
        self.exchange_name = exchange_name
        self.symbol = symbol
        self.timeframe = timeframe
        self.filename = filename
        self.exchange = getattr(ccxt, self.exchange_name)()

    def fetch_data(self):
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename, index_col='time', parse_dates=True)
            since = self.exchange.parse8601(df.index[-1].isoformat())
        else:
            df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
            since = self.exchange.milliseconds() - 1000 * 60 * 60 * 24 * 30  # 默认获取最近30天的数据
        limit = 1000  # 获取数据的数量限制
        while True:
            try:
                data = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since, limit)
                new_df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
                new_df['time'] = pd.to_datetime(new_df['time'], unit='ms')  # Convert timestamp to datetime
                new_df.set_index('time', inplace=True)  # Set datetime as index
                df = pd.concat([df, new_df])
                df.to_csv(self.filename)
                break
            except ccxt.NetworkError as e:
                print(e)
                time.sleep(self.exchange.rateLimit / 1000)
            except ccxt.ExchangeError as e:
                print(e)
                break
        return df

    def save_and_load_data(self):
        try:
            df = pd.read_csv(self.filename, index_col='time', parse_dates=True)
        except FileNotFoundError:
            print(f"No such file or directory: '{self.filename}'")
            df = None
        return df
