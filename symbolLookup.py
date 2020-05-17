from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import html5lib
import requests



stock_tickers = {'google': 'GOOGL', 'mærsk': 'MAERSK-A.CO', 'mærsk a': 'MAERSK-A.CO', 'mærsk b': 'MAERSK-B.CO', 'maersk': 'MAERSK-A.CO',}

# Searches for name - returns Symbol. EG: Apple -> AAPL
def stock_lookup(name):
    if name not in stock_tickers:
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
    else:
        return stock_tickers[name.lower()]


def forex_lookup(name):
    try:
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
        symbol = ''
        symbolRev = ''
        if ' ' in name:
                nameSplit = name.split(' ')
                if len(nameSplit) > 2:
                    index = 0
                    for i in range(len(nameSplit)):
                        if 'new' in nameSplit[i].lower():
                            index = i
                    p1 = str(nameSplit[index]) + ' ' + nameSplit[index+1]
                    nameSplit.remove(nameSplit[index+1])
                    nameSplit.remove(nameSplit[index])
                    p2 = str(''.join(nameSplit))
                    p1 = valutaSymbolsLookup(p1)['code']
                    p2 = valutaSymbolsLookup(p2)['code']
                else:
                    p1 = valutaSymbolsLookup(nameSplit[0])['code']
                    p2 = valutaSymbolsLookup(nameSplit[1])['code']
                print(p2, p1)
                symbol = str(p1)+str(p2)
                symbolRev = str(p2)+str(p1)
                print(symbol, symbolRev)
        else:
            symbol = valutaSymbolsLookup(name)['code']
        for res in results:
            if len(symbolRev) > 1:
                if symbolRev in res['symbol']:
                    return res['symbol']
            if symbol in res['symbol']:
                return res['symbol']
            else:
                return symbol
    except:
        return 'Invalid currency'
        

def valutaSymbolsLookup(name):
    try:
        URL = 'https://www.xe.com/symbols.php'
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
            result['currency'] = cols[0]
            result['code'] = cols[1]
            results.append(result)
        for res in results:
            if name.lower() in res['code'].lower() or name.lower() in res['currency'].lower():
                return res
    except:
        return 'Invalid currency'


def forex_getNameFromSymbol(symbol):
    p1 = symbol[:3]
    p2 = symbol[3:]
    v1 = valutaSymbolsLookup(p1)
    v2 = valutaSymbolsLookup(p2)
    return v1['currency'] + ' vs ' + v2['currency']

def stock_getNameFromSymbol(symbol, name):
    stock_nameDict = {value:key for key, value in stock_tickers.items()}
    if symbol not in stock_nameDict:
        return str(stock_nameLookup(symbol, name))
    else:
        return stock_tickers[stock_nameDict[symbol]]

def stock_nameLookup(symbol, name):

    URL = 'https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup='+str(name)+'&Country=all&Type=Stock'
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
        result['name'] = cols[1]
        results.append(result)
    for res in results:
        if symbol.upper() == str(res['symbol']).upper():
            return res['name']
    return results[0]['name']

