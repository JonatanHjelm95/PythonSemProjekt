import matplotlib.pyplot as plt, mpld3
import dataHandler
import numpy as np
from datetime import datetime, timedelta
import time
import symbolLookup

def convertToDate(ts):
    dateString = str(datetime.fromtimestamp(int(ts)))
    dateSplit = dateString.split(' ')
    return dateSplit[0]

def create_graph(name, _type):
    latestData, predictionData, confidence, method, title = dataHandler.getPriceData(_type, name.lower())
    # Converting list of dicts in to 2 seperate lists *2
    latestDates, latestPrices = [list(col) for col in zip(*[d.values() for d in latestData])]
    predictionDates, predictionPrices = [list(col) for col in zip(*[p.values() for p in predictionData])]
    
    for p in predictionPrices:
        latestPrices.append(p)
    for d in predictionDates:
        latestDates.append(d)
    
    dates  = []
    for l in latestDates:
        dates.append(convertToDate(l))

    x = dates
    xi = list(range(len(x)))
    plt.figure(figsize=(20,5))
    plt.xticks(xi, x)
    plt.plot(latestPrices, 'ks-')
    plt.tight_layout()
    plt.title(createTitle(_type, title)+ ', ' + str(method) +', Confidence: '+ str(round(float(confidence),2)))
    plt.setp(plt.xticks()[1], rotation=30)
    
    #plt.plot(predictionPrices)
    mpld3.show()
    

def createTitle(_type, symbol):
    if _type == 'STOCK':
        return symbolLookup.stock_getNameFromSymbol(symbol)
    if _type == 'FOREX':
        return symbolLookup.forex_getNameFromSymbol(symbol)
    if _type == 'CRYPTO':
        return symbol

if __name__ == "__main__":
    create_graph('usd denmark', 'FOREX')
    #print(convertToDate(1589061600))