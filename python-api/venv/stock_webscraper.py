from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import html5lib
import requests
from datetime import date
import symbolLookup
import time
import pandas as pd

def do_scrape(name):
    today = dateToday()
    symbol = getTickerSymbol(name)
    URL = 'https://finance.yahoo.com/quote/'+symbol+'/history?period1=1262304000&period2='+str(today)+'&interval=1d&filter=history&frequency=1d'
    req = Request(URL+str(name))
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

def getTickerSymbol(name):
    try:
        return symbolLookup.stock_lookup(name)
    except:
        return 'Invalid Stock'

def downloadCSV(name):
    today = dateToday()
    symbol = getTickerSymbol(name)
    print(symbol)
    #URL = 'https://finance.yahoo.com/quote/'+symbol+'/history?period1=1262304000&period2='+str(today)+'&interval=1d&filter=history&frequency=1d'
    URL = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(symbol)+'?period1=0&period2='+str(today)+'&interval=1d&events=history'
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
    pass
    #prices = downloadCSV('novo nordisk')
    #print(prices)
    #print(do_scrape('tesla'))
    #print(dateToday())
    #collectData('bitcoin')
    #print(getLatestPrices('bitcoin'))
    #print(do_scrape_improved('bitcoin'))
