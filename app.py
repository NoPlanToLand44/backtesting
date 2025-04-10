from flask import Flask, request, jsonify, render_template
import datetime
import os
from backtest_module import run_backtest

app = Flask(__name__)
@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        # Extract data from inputs from the HTML form 
        ticker = request.form['ticker'].strip().upper()
        start_date = request.form['start_date'] 
        end_date = request.form['end_date'] 
        capital = float(request.form['capital'])
        strategy = request.form['strategy']

        #run the strategy 
        results = run_backtest(ticker, capital, strategy, start_date, end_date) 
        # compare to buy and hold: 
        buy_and_hold = run_backtest(ticker, capital, "buy_and_hold", start_date, end_date) 
        return render_template('results.html', strategy = strategy,ticker = ticker, capital = capital, 
                               start_date = start_date, end_date = end_date, results = results, buy_and_hold = buy_and_hold)

    if request.method == 'GET':
        # Render the initial form
        return render_template('index.html')
    if __name__ == "__main__": 
        app.run(host = "0.0.0.0", port = 5000)