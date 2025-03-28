from flask import Flask, request, jsonify, render_template
import datetime
import os
# from backtest_module import run_backtest # TODO implement this function in price_data.py

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
        # results = run_backtest(ticker, start_date, end_date, capital, strategy) // import this function from price_data.py
        return render_template('results.html', results=results, ticker = ticker, start_date = start_date, end_date = end_date, capital = capital)
    if request.method == 'GET':
        # Render the initial form
        return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)
