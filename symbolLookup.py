from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import html5lib
import requests


def stock_lookup(name):
    URL = 'https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup='+name+'&Country=all&Type=Stock'
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

if __name__ == "__main__":
    print(stock_lookup('amazon'))