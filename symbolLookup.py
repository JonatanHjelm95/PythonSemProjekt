from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import html5lib
import requests

# Searches for name - returns Symbol. EG: Apple -> AAPL
def stock_lookup(name):
    query = name
    if ' ' in query:
        query=query.replace(' ','+')
    URL = 'https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup='+str(query)+'&Country=all&Type=Stock'
    req = Request(URL)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html5lib')
    tbody = soup.find('tbody')
    row = tbody.find_all('tr')
    results = []
    for r in row:
        result = {}
        cols = r.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        result['symbol'] = cols[0]
        result['name']  =cols[1]
        results.append(result)
    for res in results:
        if name in str(res['name']).lower():
            return res['symbol']
    return results[0]['symbol']


def forex_lookup(name):
    URL = 'https://www.instaforex.com/trading_symbols'
    req = Request(URL)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html5lib')
    tbody = soup.find('tbody')
    row = tbody.find_all('tr')
    results = []
    for r in row:
        result = {}
        cols = r.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        result['symbol'] = cols[0]
        # Webpage has typo in New Zealand
        if 'New Zeland' in cols[1]:
            result['name'] = 'New Zealand Dollar'
        else:
            result['name'] =cols[1]
        results.append(result)
    #return results
    for res in results:
        print(compareSet(name, res['symbol']))


def compareSet(name, forexSymbol):
    if ' ' in name:
        nameSet = set(name.lower().split(' '))
        forexSet = set(forexSymbol[0:3].lower()+ forexSymbol[3:6].lower())
        return nameSet == forexSet



if __name__ == "__main__":
    print(stock_lookup('mazda'))
    #print(forex_lookup('usd dkk'))
    
    #print(stock_lookup('amazon'))