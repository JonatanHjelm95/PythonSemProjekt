from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import html5lib
import requests
from datetime import date
import symbolLookup
import time
import pandas as pd


def getTickerSymbol(name):
    try:
        return symbolLookup.forex_lookup(name)
    except:
        return 'Invalid Currency'

def downloadCSV(name):
    name = name.replace(' ','+')
    today = dateToday()
    symbol = getTickerSymbol(name)
    print(symbol)
    #URL = 'https://finance.yahoo.com/quote/'+symbol+'/history?period1=1262304000&period2='+str(today)+'&interval=1d&filter=history&frequency=1d'
    #URL = 'https://query1.finance.yahoo.com/v7/finance/download/'+symbol+'?period1=0&period2='+str(today)+'&interval=1d&events=history'
    #URL = 'https://finance.yahoo.com/quote/'+str(symbol)+'%3DX/history?period1=0&period2='+str(today)+'&interval=1d&filter=history&frequency=1d'
    URL = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(symbol)+'=X?period1=0&period2='+str(today)+'&interval=1d&events=history'
    print(URL)
    req = requests.get(URL)
    url_content = req.content
    csv_file = open('downloaded.csv', 'wb')
    csv_file.write(url_content)
    csv_file.close()
    prices = pd.read_csv('downloaded.csv')
    title = symbol
    prices.dropna(how='any', inplace=True)
    return prices[::-1], title



def dateToday():
    today = date.today()
    ts = time.mktime(today.timetuple())
    return int(ts)


if __name__ == '__main__':
    prices = downloadCSV('sweden denmark')
    #print(prices)
    #print(do_scrape('tesla'))
    #print(dateToday())
    #collectData('bitcoin')
    #print(getLatestPrices('bitcoin'))
    #print(do_scrape_improved('bitcoin'))
