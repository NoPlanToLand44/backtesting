import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import backtrader as bt
import datetime 
import os 
import strategy_module as sm
from fetching_data import fetch_stock_data

STRATEGY_CONFIG = {
    "buy_and_hold" :{
        "strategy_class":sm.buy_and_hold,
        "analyzers": ["returns","drawdown","sharpe"],
        "sizer" : {"percents" : 100}
    },
    "sma_cross" : {
        "strategy_class":sm.SmaCrossStrategy,
        "analyzers": ["returns","drawdown", "sharpe"],
        "sizer" : {"percents" : 5}
    },
    "boll_reversion_to_mean" : {
        "strategy_class":sm.BollingerMeanReversionStrategy,
        "analyzers": ["returns","drawdown", "sharpe"],
        "sizer" : {"percents" : 20}
    },
    "MACDCrossoverStrategy": {
        "strategy_class":sm.MACDCrossoverStrategy,
        "analyzers": ["returns", "drawdown","sharpe"],
        "sizer": {"percents": 20}
    },
    "RSIReversalStrategy": {
        "strategy_class":sm.RSIReversalStrategy,
        "analyzers": ["returns", "drawdown","sharpe"],
        "sizer": {"percents": 20}
    }
}


def run_backtest(ticker, capital, strategy, start_date = datetime.datetime.now() - datetime.timedelta(days = 356), 
                 end_date = datetime.datetime.now()):
    try:
        df = fetch_stock_data(ticker = ticker, start_date = start_date, end_date = end_date)
        data_feed = bt.feeds.PandasData(dataname = df)
    except Exception as e: 
        return{"error": f"failed data: {str(e)}"}   
    if strategy not in STRATEGY_CONFIG:
        return {"error": "unknown stategy"}

    carebro = bt.Cerebro()
    carebro.adddata(data_feed)
    carebro.broker.setcash(capital)
    
    config = STRATEGY_CONFIG[strategy]
    carebro.addstrategy(config["strategy_class"])

    carebro.addsizer(bt.sizers.PercentSizer,**config['sizer'])

    # add analyzers: 
    if "returns" in config["analyzers"]: 
        carebro.addanalyzer(bt.analyzers.Returns, _name = 'returns')
    if "sharpe" in config['analyzers']:
        carebro.addanalyzer(bt.analyzers.SharpeRatio, _name = "sharpe")
    if "drawdown" in config['analyzers']:
        carebro.addanalyzer(bt.analyzers.DrawDown, _name = "drawdown")
    
    try: 
        results = carebro.run()
        if not results or len(results) == 0 :
            return {"error" : "strategy produced nothing "}
        results_dict = {
            "final_value": round(carebro.broker.getvalue(),2)
        }
        if 'returns' in config['analyzers']:
            results_dict['returns'] = round(results[0].analyzers.returns.get_analysis()['rtot'] * capital,2)
        if "sharpe" in config['analyzers']: 
            results_dict['sharpe'] = round(results[0].analyzers.sharpe.get_analysis()['sharperatio'],2)
        if "drawdown" in config['analyzers']:
            results_dict['drawdown'] = round(results[0].analyzers.drawdown.get_analysis()['max']['drawdown'],2)
        
        return results_dict
    except Exception as e: 
        return {"error": f"strategy exec failed: {str(e)}"}