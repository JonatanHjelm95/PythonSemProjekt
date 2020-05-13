import matplotlib.pyplot as plt, mpld3
import dataHandler
import numpy as np
from datetime import datetime, timedelta
import time

def convertToDate(ts):
    dateString = str(datetime.fromtimestamp(int(ts)))
    dateSplit = dateString.split(' ')
    return dateSplit[0]

def create_graph(name):
    latestData, predictionData, confidence, method = dataHandler.getPriceData('CRYPTO', name)
    # Converting list of dicts in to 2 seperate lists
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
    plt.title(name+ ', ' + str(method) +', Confidence: '+ str(round(float(confidence),2)))
    plt.setp(plt.xticks()[1], rotation=30)
    
    #plt.plot(predictionPrices)
    mpld3.show()
    




if __name__ == "__main__":
    create_graph('bitcoin')
    #print(convertToDate(1589061600))