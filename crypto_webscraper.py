from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date

def do_scrape(crypto):
    today = dateToday()
    URL = 'https://coinmarketcap.com/currencies/'+str(crypto)+'/historical-data/?start=20130429&end='+str(today)
    req = Request(URL+str(crypto))
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html5lib')
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')
    ClosePrices = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        date = cols[0]
        date = date.replace(',', '')
        close = cols[4]
        close = close.replace(',','')
        #closePrice['price'] = float(close)
        ClosePrices.append(float(close))
    return ClosePrices


def dateToday():
    today = date.today()
    today = str(today).replace('-','')
    return today

if __name__ == '__main__':
    do_scrape('bitcoin')
