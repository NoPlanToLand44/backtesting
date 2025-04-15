import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import backtrader as bt
import datetime
import os
from  strategy_module import buy_and_hold, SmaCrossStrategy # import the strategies from strategy_module.py
from  fetching_data import fetch_stock_data



def run_backtest(ticker, capital, strategy, start_date = datetime.datetime.now() - datetime.timedelta(days = 365), end_date = datetime.datetime.now()):
    try:
        df = fetch_stock_data(ticker = ticker, start_date=start_date, end_date=end_date)
        data_feed = bt.feeds.PandasData(dataname = df)
    except Exception as e:
        return {"error" : f"failed data: {str(e)}"}

    if strategy == 'buy_and_hold':
        carebro2 = bt.Cerebro()# the class that will handle the backtesting 
        carebro2.adddata(data_feed)  # carebro takes in a feed from a backtrader pandas DF 
        carebro2.broker.setcash(capital) # might want to expose that to the user later
        carebro2.addstrategy(buy_and_hold)
        carebro2.addsizer(bt.sizers.PercentSizer, percents = 10) # 10% of the cash will be used for each trade
        carebro2.addanalyzer(bt.analyzers.Returns)
        carebro2.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        results2 = carebro2.run()
        return {
            "final_value": carebro2.broker.getvalue(),
            "returns": results2[0].analyzers.returns.get_analysis()["rtot"]*capital,
            "max_drawdown": results2[0].analyzers.drawdown.get_analysis()['max']['drawdown']
        }

    if strategy == 'sma_cross':
        carebro = bt.Cerebro()# the class that will handle the backtesting 
        carebro.adddata(data_feed)  # carebro takes in a feed from a backtrader pandas DF 
        carebro.broker.setcash(capital) # might want to expose that to the user later
        carebro.addstrategy(SmaCrossStrategy)
        carebro.addsizer(bt.sizers.PercentSizer, percents = 10) # 10% of the cash will be used for each trade
        carebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        carebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'sharpe')
        carebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        try:
            results = carebro.run()
            if not results or len(results) == 0: 
                return {"error": "strategy produced no results"}
            return {
                "final_value": carebro.broker.getvalue(),
                "returns": results[0].analyzers.returns.get_analysis()["rtot"]*capital,
                "sharpe_ratio": results[0].analyzers.sharpe.get_analysis()["sharperatio"],
                "max_drawdown": results[0].analyzers.drawdown.get_analysis()['max']['drawdown'],
            }
        except IndexError as e:
            return {"error": f"strategy execution failed: {str(e)}"}
    else:
        return {"error": f"unknown strategy"}