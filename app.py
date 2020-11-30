from flask import Flask, request, render_template, jsonify
import json
import os
import time
#import random
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from product import Product
from utils import convert_price_toNumber

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-text', methods=['GET', 'POST'])
def foo():

    print("")
    print("#####################################")
    start_time = time.time()

    bar = request.form['test']
    
    URL = "http://www.amazon.com/"
    NUMBER_OF_PAGES_TO_SEARCH = 2
    QUESTION_PRODUCT = "What are you looking for?\n:"
    PRODUCT_PATH = '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div'
    #ELEMENT_ID = '//*[@id="twotabsearchtextbox"]'
    ELEMENT_ID = "//input[@type='text'][@id='twotabsearchtextbox']"
    search_term = str(bar)

    biggest_discount = 0.0
    lowest_price = 0.0
    chepest_product = Product("", "", "", "", "", "")
    best_deal_product = Product("", "", "", "", "", "")
    search_terms = search_term.split(" ")

    print("")
    print("--- DRIVER STARTED ---")
    print("--- %s seconds ---" % (time.time() - start_time))

    # GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google_chrome' #PATH SET ON HEROKU CONFIG_VARS
    # CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver' #PATH SET ON HEROKU CONFIG_VARS

    #####################################
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") #UNCOMMENT FOR DEPLOYMENT/COMMENT FOR TESTING
    #####################################
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    #####################################
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options) #UNCOMMENT FOR DEPLOYMENT
    #driver = webdriver.Chrome("D:\chromedriver.exe", options=options) ##UNCOMMENT FOR TESTING (SET DRIVERT PATH)
    #####################################

    # headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WIN64; x64) AppleWebKit/537.36 Chrome/87.0.4280.66 Safari.537,36'}
    # proxies_list = ["128.199.109.241:8080","113.53.230.195:3128","125.141.200.53:80","125.141.200.14:80","128.199.200.112:138","149.56.123.99:3128","128.199.200.112:80","125.141.200.39:80","134.213.29.202:4444"]
    # proxies = {'https': random.choice(proxies_list)}
    # time.sleep(0.5 * random.random())
    
    driver.header_overrides = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WIN64; x64) AppleWebKit/537.36 Chrome/87.0.4280.66 Safari.537,36'}

    driver.get(URL)
    time.sleep(5)

    print("")
    print("--- SCRAPING... ---")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("")
    
    element = driver.find_element_by_xpath(ELEMENT_ID)
    element.send_keys(search_term)
    element.send_keys(Keys.ENTER)

    products = []

    page = NUMBER_OF_PAGES_TO_SEARCH

    print("--- PAGES SCRAPED ---")
    print(page)
    while True:
        if page != 0:
            try:
                driver.get(driver.current_url + "&page=" + str(page))
            except:
                break
        
        for i in driver.find_elements_by_xpath(PRODUCT_PATH):
            should_add = True
            name = ""
            price = ""
            prev_price = ""
            link = ""
            discount = 0.0
            # rating = ""
            prime = False
            try:
                h2tag = i.find_element_by_tag_name('h2')
                name = h2tag.text
                price = convert_price_toNumber(i.find_element_by_class_name('a-price').text)
                link = h2tag.find_element_by_tag_name('a').get_attribute("href")
                # rating = 
                try:
                    prime_element = i.find_element_by_class_name("a-icon-prime")
                    #print(prime_element)
                    prime = True
                except:
                    Exception()
                try:
                    prev_price = convert_price_toNumber(i.find_element_by_class_name('a-text-price').text)
                    discount = (prev_price-price)/prev_price*100
                except:
                    Exception()
                    prev_price = price
            except:
                # print("exception")
                should_add = False
            
            product = Product(name, price, prev_price, discount, link, prime)
            if should_add:
                products.append(product)
                # print(products)
                
        page = page - 1
        if page == 0:
            break
        print(page)
    
    driver.quit()
    
    print("")
    print("--- DRIVER SUCCESS... STARTING SORTER ---")
    print("--- %s seconds ---" % (time.time() - start_time))
    
    run = 0
    for product in products:
        not_right = False
        # for word in search_terms:
        #     if word.lower() not in product.name.lower():
        #         not_right = True
        if not not_right:
            if run == 0:
                lowest_price = product.price
                chepest_product = product
                run = 1
            elif product.price < lowest_price:
                lowest_price = product.price
                chepest_product = product
            if product.discount > biggest_discount:
                biggest_discount = product.discount
                #print(product.discount)
                best_deal_product = product

    data = {}
    data["Products"] = []
    for prod in products:
        data["Products"].append(prod.serialize())
    
    # with open('products.json', 'w') as json_file:
    #     data = {}
    #     data["Products"] = []
    #     for prod in products:
    #         data["Products"].append(prod.serialize())
    #     json.dump(data, json_file, sort_keys=True, indent=4)

    # print(json.dumps(chepest_product.serialize(), indent=4, sort_keys=True))
    # print(json.dumps(best_deal_product.serialize(), indent=4, sort_keys=True))

    # options = webdriver.ChromeOptions()
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # ##############################
    # options.add_argument('--headless')
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # #options.add_argument("--disable-gpu")
    # ##############################
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    # #driver = webdriver.Chrome("chromedriver.exe", options=options)
    # ##############################

    # driver.get(best_deal_product.link)
    # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

    print("")
    print("--- SESSION COMPLETE ---")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("")
    print("#####################################")
    return jsonify(data)

    return (driver.get(URL))

if __name__ == '__main__':
    app.run(debug=True)