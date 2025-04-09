import backtrader as bt
import datetime
import os


class buy_and_hold(bt.Strategy):
        def next(self):
            self.buy()

class SmaCrossStrategy(bt.Strategy):
        params = (('fast', 20),('slow', 200),('mega_slow', 500), ) # parameters for the strategy
        def __init__(self):
            self.sma_fast = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.fast)
            self.sma_slow = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.slow)
            self.sma_super_slow = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.mega_slow)
            self.crossover_fs = bt.indicators.CrossOver(self.sma_fast, self.sma_slow) # crossover signal
            self.crossover_ss = bt.indicators.CrossOver(self.sma_slow, self.sma_super_slow) # crossover signal

    # add more indicators classes here RSI, MACD, etc.

        def next(self):
            # if we are not in a position and a golder cross occurs, buy
            if not self.position: # self.postion = 0 when we are not in a position
                if self.crossover_fs > 0: # self.crossover_fs = 1 when the fast sma crosses the slow sma from below
                    self.buy()  # buy the stock
            else : 
                if self.crossover_fs < 0: # self.crossover_fs = -1 when the fast sma crosses the slow sma from above  
                    self.sell()
