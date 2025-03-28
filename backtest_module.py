import pandas as pd 
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import backtrader as bt
import datetime
import os


ticker = 'NVDA'
# getting the last 5 years of data until current date
data = yf.download(ticker, start = datetime.datetime.now() - datetime.timedelta(1500), end = datetime.datetime.now())
data.columns = data.columns.droplevel([1]) # clear the multi-index columns
data_feed = bt.feeds.PandasData(dataname = data)
carebro = bt.Cerebro()# the class that will handle the backtesting 
carebro.adddata(data_feed)  # carebro takes in a feed from a backtrader pandas DF 
carebro.broker.setcash(10000) # might want to expose that to the user later

class SmaCrossStrategy(bt.Strategy):
    params = (('fast', 1),('slow', 200),('mega_slow', 500), ) # parameters for the strategy
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
        # add more conditions here for more indicators
            
class buy_and_hold(bt.Strategy):
    def next(self):
        self.buy()

carebro.addstrategy(SmaCrossStrategy)
carebro.addsizer(bt.sizers.PercentSizer, percents = 10) # 10% of the cash will be used for each trade
carebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'sharpe')
results = carebro.run()
carebro2 = bt.Cerebro()# the class that will handle the backtesting 
carebro2.adddata(data_feed)  # carebro takes in a feed from a backtrader pandas DF 
carebro2.broker.setcash(10000) # might want to expose that to the user later
carebro2.addstrategy(buy_and_hold)
carebro2.addsizer(bt.sizers.PercentSizer, percents = 100) # 10% of the cash will be used for each trade
results2 = carebro2.run()
final_value = carebro.broker.getvalue()
final_value2 = carebro2.broker.getvalue()
print(f'Final value from strat1 : {final_value}')
print(f'Final value from strat2 : {final_value2}')
sharp = results[0].analyzers.sharpe.get_analysis()
sharp




