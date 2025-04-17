from flask import Flask, request, jsonify, render_template, redirect
import logging 
import datetime
import os
from backtest_module import run_backtest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        # Extract data from inputs from the HTML form 
        try:
            ticker = request.form['ticker'].strip().upper()
            start_date = datetime.datetime.strptime(request.form['start_date'], '%Y-%m-%d') 
            end_date = datetime.datetime.strptime(request.form['end_date'], '%Y-%m-%d')
            capital = float(request.form['capital'])
            strategy = request.form['strategy']

            #run the strategy 
            results = run_backtest(ticker, capital, strategy, start_date, end_date) 
            # compare to buy and hold: 
            if  strategy == "buy_and_hold" :
                buy_and_hold = results
                show_comparison = False
            else:
                buy_and_hold = run_backtest(ticker, capital, "buy_and_hold", start_date, end_date)
                show_comparison = True
            return render_template( 'results.html', 
                                    strategy = strategy,
                                    ticker = ticker,
                                    capital = capital, 
                                    start_date = start_date,
                                    end_date = end_date,
                                    results = results,
                                    buy_and_hold = buy_and_hold,
                                    show_comparison = show_comparison)
        except Exception as e:
            logger.error(f"unandled exception: {str(e)}")
            return render_template("error.html", error = str(e))
    if request.method == 'GET':
        # Render the initial form
        return render_template('index.html')
if __name__ == "__main__": 
    app.run(host = "0.0.0.0", port = 5000)
    # some shit  saddsdsd