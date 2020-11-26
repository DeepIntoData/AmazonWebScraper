from flask import Flask, request, render_template, jsonify
import requests 
import json
import os

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from product import Product
from utils import convert_price_toNumber
from web_driver_conf import get_web_driver_options
from web_driver_conf import get_chrome_web_driver
from web_driver_conf import set_ignore_certificate_error
from web_driver_conf import set_browser_as_incognito
from web_driver_conf import set_automation_as_head_less

#from price_scraper import FUNCTION NAME

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-text', methods=['GET', 'POST'])
def foo():

    bar = request.form['test']
    
    URL = "http://www.amazon.com/"
    NUMBER_OF_PAGES_TO_SEARCH = 5
    QUESTION_PRODUCT = "What are you looking for?\n:"
    search_term = str(bar) #PASS USER INPUT FROM HTML TO HERE

    biggest_discount = 0.0
    lowest_price = 0.0
    chepest_product = Product("", "", "", "")
    best_deal_product = Product("", "", "", "")
    search_terms = search_term.split(" ")

    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    driver.get(URL)
    element = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    element.send_keys(search_term)
    element.send_keys(Keys.ENTER)
    products = []
    page = NUMBER_OF_PAGES_TO_SEARCH

    while True:
        if page != 0:
            try:
                driver.get(driver.current_url + "&page=" + str(page))
            except:
                break

        for i in driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]'):
            counter = 0
            for element in i.find_elements_by_xpath('//div/span/div/div/div/div'):
                should_add = True
                name = ""
                price = ""
                prev_price = ""
                link = ""
                try:
                    name = i.find_elements_by_tag_name('h2')[counter].text
                    price = convert_price_toNumber(element.find_element_by_class_name('a-price').text)
                    link = i.find_elements_by_xpath('//h2/a')[counter].get_attribute("href")
                    try:
                        prev_price = convert_price_toNumber(element.find_element_by_class_name('a-text-price').text)
                    except:
                        Exception()
                        prev_price = price
                except:
                    print("exception")
                    should_add = False
                product = Product(name, price, prev_price, link)
                if should_add:
                    products.append(product)
                    print(products)
                counter = counter + 1
        page = page - 1
        if page == 0:
            break
        print(page)
    run = 0

    for product in products:
        not_right = False
        for word in search_terms:
            if word.lower() not in product.name.lower():
                not_right = True
        if not not_right:
            if run == 0:
                lowest_price = product.price
                chepest_product = product
                run = 1
            elif product.price < lowest_price:
                lowest_price = product.price
                chepest_product = product
            discount = product.prev_price - product.price
            if discount > biggest_discount:
                biggest_discount = discount
                best_deal_product = product

    with open('products.json', 'w') as json_file:
        data = {}
        data["Products"] = []
        for prod in products:
            data["Products"].append(prod.serialize())
        json.dump(data, json_file, sort_keys=True, indent=4)

    print(json.dumps(chepest_product.serialize(), indent=4, sort_keys=True))
    print(json.dumps(best_deal_product.serialize(), indent=4, sort_keys=True))

    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    driver.get(best_deal_product.link)
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

    return jsonify(data)

if __name__ == '__main__':
    app.run()