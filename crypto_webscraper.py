from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import html5lib
import requests
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
        dataPoint = {}
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        date = cols[0]
        date = date.replace(',', '')
        close = cols[4]
        close = close.replace(',','')
        dataPoint['close'] = float(close)
        dataPoint['date'] = date
        ClosePrices.append(dataPoint)
    return ClosePrices


def do_scrape_improved(crypto):
    today = dateToday()
    URL = 'https://coinmarketcap.com/currencies/'+str(crypto)+'/historical-data/?start=20130429&end='+str(today)
    req = Request(URL+str(crypto))
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html5lib')
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')
    Prices = []
    for row in rows:
        dataPoint = {}
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        date = cols[0]
        date = date.replace(',', '')
        opn = cols[1]
        opn = opn.replace(',','')
        high = cols[2]
        high = high.replace(',','')
        low = cols[3]
        low = low.replace(',','')
        close = cols[4]
        close = close.replace(',','')
        dataPoint['open'] = float(opn)
        dataPoint['high'] = float(high)
        dataPoint['low'] = float(low)
        dataPoint['close'] = float(close)
        dataPoint['date'] = date
        Prices.append(dataPoint)
    return Prices

def getLatestPrices(name):
    symbol = getTickerSymbol(name)
    url = 'https://api-pub.bitfinex.com/v2/tickers?symbols='+str(symbol)
    r = requests.get(url)
    data = r.json()
    prices = {'high': float(data[0][9]), 'low': float(data[0][10])}
    return prices

def getTickerSymbol(name):
    tickers = {'bitcoin': 'tBTCUSD', 'ethereum': 'tETHUSD'}
    try:
        return tickers[name.lower()]
    except Exception as e:
        print(e)

def dateToday():
    today = date.today()
    today = str(today).replace('-','')
    return today

def collectData(name):
    prices = do_scrape_improved(name)
    latestPrices = getLatestPrices(name)
    dataPoint = {}
    dataPoint['open'] = prices[0]['close']
    dataPoint['high'] = latestPrices['high']
    dataPoint['low'] = latestPrices['low']
    dataPoint['close'] = latestPrices['high']
    dataPoint['date'] = 'now'
    prices = prices[::-1]
    prices.append(dataPoint)
    prices = prices[::-1]
    return prices

def appendLatestData():
    pass
if __name__ == '__main__':
    collectData('bitcoin')
    #print(getLatestPrices('bitcoin'))
    #print(do_scrape_improved('bitcoin'))
