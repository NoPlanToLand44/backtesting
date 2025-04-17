import backtrader as bt
import datetime
import os


class buy_and_hold(bt.Strategy):
    def next(self):
        if not self.position:
            self.buy()

class SmaCrossStrategy(bt.Strategy):
    params = (('fast', 20),('slow', 50),('mega_slow', 200), ) # parameters for the strategy
    def __init__(self):
        self.sma_fast = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.fast)
        self.sma_slow = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.slow)
        self.sma_super_slow = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.mega_slow)
        self.crossover_fs = bt.indicators.CrossOver(self.sma_fast, self.sma_slow) # crossover signal
        self.crossover_ss = bt.indicators.CrossOver(self.sma_slow, self.sma_super_slow) # crossover signal
        self.min_period = max(self.params.fast, self.params.slow, self.params.mega_slow)

# add more indicators classes here RSI, MACD, etc.

    def next(self):
        if len(self) <= self.min_period:
                return
        # if we are not in a position and a golder cross occurs, buy
        if not self.position: # self.postion = 0 when we are not in a position
            if self.crossover_fs > 0: # self.crossover_fs = 1 when the fast sma crosses the slow sma from below
                self.buy()  # buy the stock
        else : 
            if self.crossover_fs < 0: # self.crossover_fs = -1 when the fast sma crosses the slow sma from above  
                self.close()

class BollingerMeanReversionStrategy(bt.Strategy):
    params = (
        ("period", 30), # can adjust
        ("devfactor", 3) #can adjust
    )
    def __init__(self):
        self.bb = bt.indicators.BollingerBands(self.data.close, period = self.p.period, devfactor = self.p.devfactor)
    def next(self):
        if self.data.close[0]<self.bb.bot[0]:
                self.buy()
        else:
            if self.data.close[0] > self.bb.top[0]:
                if self.position.size>0:
                    self.sell()

class MACDCrossoverStrategy(bt.Strategy):
    params = (
        ("fast", 12),
        ("slow", 26),
        ("signal", 9 )
    )
    def __init__(self):
        self.macd = bt.indicators.MACD(
        self.data.close,
        period_me1 = self.p.fast,
        period_me2 = self.p.slow,
        period_signal = self.p.signal
        )
        # determine the crossover period: 
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
    
    def next(self):
        if self.crossover > 0:
            self.buy()
        elif self.position and self.crossover < 0:
            self.sell()

class RSIReversalStrategy(bt.Strategy):
    params = (
        ('period', 14),      # period for the RSI calculation
        ('oversold', 30),    # RSI level considered oversold
        ('overbought', 70),  # RSI level considered overbought
    )

    def __init__(self):
        # Compute the Relative Strength Index.
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data.close, period=self.p.period)

    def next(self):
        if self.rsi[0] < self.p.oversold:
            self.buy()
        elif self.position and self.rsi[0] > self.p.overbought:
            self.sell()
