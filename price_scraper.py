import requests 
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from product import Product
from utils import convert_price_toNumber

    bar = request.form['test']
    
    URL = "http://www.amazon.com/"
    NUMBER_OF_PAGES_TO_SEARCH = 1
    QUESTION_PRODUCT = "What are you looking for?\n:"
    PRODUCT_PATH = '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div'
    search_term = str(bar)

    biggest_discount = 0.0
    lowest_price = 0.0
    chepest_product = Product("", "", "", "", "", "")
    best_deal_product = Product("", "", "", "", "", "")
    search_terms = search_term.split(" ")

    #####################################
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    #####################################

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
                    print(prime_element)
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
                print(product.discount)
                best_deal_product = product

    with open('products.json', 'w') as json_file:
        data = {}
        data["Products"] = []
        for prod in products:
            data["Products"].append(prod.serialize())
        json.dump(data, json_file, sort_keys=True, indent=4)

    print(json.dumps(chepest_product.serialize(), indent=4, sort_keys=True))
    print(json.dumps(best_deal_product.serialize(), indent=4, sort_keys=True))

    ##############################
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    ##############################

    driver.get(best_deal_product.link)
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')