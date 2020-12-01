<h1 align="center">Amazon Web Scraper</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />
  <a href="1" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://opensource.org/licenses/MIT" target="_blank">
    <img alt="License: MIT--License" src="https://img.shields.io/badge/License-MIT--License-yellow.svg" />
  </a>
</p>

>A Flask enabled Web Scraping Service to find best product deals on Amazon
***

## ✨ Demo

<p align="center">
  <img width="800" align="center" src="https://raw.githubusercontent.com/Frozte/AmazonWebScraper/main/demo.PNG" alt="demo"/>
</p>

Visit the link 🔗[HERE](https://amazonwebscraper.herokuapp.com/) to try out the scrape for yourself. Please be patient as the process takes a bit to run in its current state.

The output will be in a .json format, after which, the user may click or copy and paste the URL into their browser.

```sh
{
  "Discount": 40.00800160032007, 
  "Name": "Just Dance 2021 Xbox Series X|S, Xbox One", 
  "Previous price": 49.99, 
  "Price": 29.99, 
  "Prime product": true, 
  "URL": "https://www.amazon.com/Just-Dance-2021-Xbox-One/dp/B08GQW447N/ref=sr_1_16?dchild=1&keywords=xbox&qid=1606806822&sr=8-16"
}

```

***
## ✔️ Prerequisites

You will need to download a chromedriver.exe compatible with your version of Google Chrome. To check your chrome version, please navigate to 'Settings>About Chrome' and note your version. Then proceed to this [link](https://chromedriver.chromium.org/) and download the driver specific to your version. Take note of the filepath of this driver for the steps in the Usage section.

Other prerequisites include...

```sh
Flask >= 1.1.2
Selenium >= 3.141
Requests >= 2.25
```
***

## 🖥️ Usage

For local usage, please navigate to the price_scraper.py file and comment/uncomment the following. Code can be found in lines 34, 42, and 43.
```sh
34: #options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
42: #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
43: driver = webdriver.Chrome("chromedriver.exe", options=options)
```
The path for the "chromedriver.exe" must also be changed according to your filepath. 

Completing the above, proceed to run the code by 

```sh
python app.py
```
---
## ⚠️ Current Issues

While code is working properly, we would like to make the process run faster. Currently, the working deployment is scraping 1 page which we wish to change to 5. However, we are limited to 500MB and about 30 secs of runtime before Heroku timesout with it's infamous H12 error. The current code runs at an average of 20secs. We are already looking for ways to make this better. For those that wish to contribute, please create a pull request and we will include you as contributors

***
## 📖 Author

👤 **Deep Patel**

* Website: www.mrdeeppatel.com
* Github: [@Frozte](https://github.com/Frozte)
* LinkedIn: [@Deep Patel](https://linkedin.com/in/deep-patel-79082494)

👤 **Joshua Coronel**

* Github: [@joshuajonme](https://github.com/joshuajonme)
* LinkedIn: [@Joshua Coronel](https://www.linkedin.com/in/joshuacoronel/)

Initial code was forked from [KalleHallden](https://github.com/KalleHallden/BlackFridayScrape)
***
## 👌 Show your support

Give a ⭐️ if this project helped you!
***
## 📝 License

Copyright © 2020 [Deep Patel](https://github.com/Frozte).<br />
This project is [MIT](https://github.com/Frozte/AmazonWebScraper/blob/main/LICENSE) licensed.

***
_This README was generated with [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_