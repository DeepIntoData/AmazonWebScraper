from price_scraper import scrape_amazon_search, best_deal
from flask import Flask, request, render_template, jsonify
import requests 
import json
import os 

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():

    search_term = str(request.form['test'])

    products = scrape_amazon_search(search_term)

    best_deal_item = best_deal(products)

    #return jsonify(products)
    return (best_deal_item)

if __name__ == '__main__':
    app.run(debug=True)