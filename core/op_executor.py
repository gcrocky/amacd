class TradingExecutor:
    def __init__(self, df):
        self.df = df
        self.total_investment = 0
        self.total_units = 0
        self.portfolio_value = []  # Track portfolio value over time

    def find_cross_points(self):
        cross_points = (self.df['macd'].shift(1) < self.df['signal'].shift(1)) & (self.df['macd'] > self.df['signal']) & (self.df['macd'] < -500)
        return cross_points

    def execute(self, stop_loss=0.95, take_profit=1.10):
        cross_points = self.find_cross_points()
        buy_price = None
        for i in range(len(self.df)):
            if cross_points.iloc[i]:  # Buy at the open price of the next bar after the cross point
                buy_price = self.df['open'].iloc[i+1] if i+1 < len(self.df) else None
                self.total_investment += buy_price
                self.total_units += 1
                print(f'Buy 1 unit at {buy_price} on {self.df.index[i+1]}')
            if buy_price is not None:
                current_portfolio_value = self.total_units * self.df['close'].iloc[i]
                self.portfolio_value.append(current_portfolio_value)
                if current_portfolio_value <= self.total_investment * stop_loss:  # Stop loss
                    print(f'Stop loss at {self.total_investment * stop_loss} on {self.df.index[i]}')
                    buy_price = None
                    self.total_investment = 0
                    self.total_units = 0
                elif current_portfolio_value >= self.total_investment * take_profit:  # Take profit
                    print(f'Take profit at {self.total_investment * take_profit} on {self.df.index[i]}')
                    buy_price = None
                    self.total_investment = 0
                    self.total_units = 0

    def calculate_return(self):
        initial_investment = self.portfolio_value[0]
        final_value = self.portfolio_value[-1]
        return (final_value - initial_investment) / initial_investment

    def calculate_max_drawdown(self):
        max_value = self.portfolio_value[0]
        max_drawdown = 0
        for value in self.portfolio_value:
            if value > max_value:
                max_value = value
            drawdown = (max_value - value) / max_value
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        return max_drawdown
# Path: core/op_strategy.py