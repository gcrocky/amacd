import os
import time
import ccxt
import pandas as pd

class op_kline():
    '''
    用于获取和保存k线数据
    '''
    def __init__(self):
        pass

    def save_and_load_data(df, filename):
        df.to_csv(filename)
        loaded_df = pd.read_csv(filename, index_col='time', parse_dates=True)
        return loaded_df

    def fetch_data(exchange_name, symbol, timeframe, filename):
        exchange = getattr(ccxt, exchange_name)()
        if os.path.exists(filename):
            df = pd.read_csv(filename, index_col='time', parse_dates=True)
            since = exchange.parse8601(df.index[-1].isoformat())
        else:
            df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
            since = exchange.milliseconds() - 1000 * 60 * 60 * 24 * 30  # 默认获取最近30天的数据
        limit = 1000  # 获取数据的数量限制
        while True:
            try:
                data = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
                new_df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
                new_df['time'] = pd.to_datetime(new_df['time'], unit='ms')  # Convert timestamp to datetime
                new_df.set_index('time', inplace=True)  # Set datetime as index
                df = pd.concat([df, new_df])
                df.to_csv(filename)
                break
            except ccxt.NetworkError as e:
                print(e)
                time.sleep(exchange.rateLimit / 1000)
            except ccxt.ExchangeError as e:
                print(e)
                break
        return df
