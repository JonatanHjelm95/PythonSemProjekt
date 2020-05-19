import matplotlib.pyplot as plt, mpld3
import dataHandler
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import symbolLookup
import os.path

def convertToDate(ts):
    dateString = str(datetime.fromtimestamp(int(ts)))
    dateSplit = dateString.split(' ')
    return dateSplit[0]

def create_graph(name, _type):
    try:
        name = name.replace(' ','+')
        latestData, predictionData, confidence, method, title = dataHandler.getPriceData(_type, name.lower())
        
        # Creating 1 dataframe from 2 lists of dicts
        df = pd.DataFrame(merge_lists_of_dicts(latestData, predictionData))
        # setting latest timestamp from the actual price data
        currentTimestamp = latestData[-1]['timestamp']
        # defining plotsize
        plt.subplots(figsize=(20,5))
        # plotting all data
        plt.plot(df['date'], df['price'], 'ks-', c = 'blue', label='Historical prices')
        # plotting prediction data on top
        plt.plot(df[df.timestamp >= currentTimestamp]['date'], df[df.timestamp >= currentTimestamp]['price'], 'ks-', c = 'red', label='Predicted prices')
        # Setting title, methods and Coef
        plt.title(createTitle(_type, title, name)+ ', ' + str(method) +', Confidence: '+ str(round(float(confidence),2)))
        # Rotating x labels
        plt.xticks(rotation = 45)
        #plt.savefig('flask-app/src/figure')
        #plt.savefig('flask-app/src/figure')
        plt.savefig('D:/Studie/4sem/PythonSemProjekt/flask-app/src/figure.png')
        #plt.show()
        return df.to_json()
    except Exception as e:
        return e
    #mpld3.save_json(fig=fig, fileobj='test')
    #return mpld3.fig_to_html(plt.figure())

    
    

def merge_lists_of_dicts(l1, l2):
    wholeData = []
    for l in l1:
        data = {}
        data['timestamp'] = l['timestamp']
        data['price'] = l['price']
        data['date'] = createDate(l['timestamp'])
        wholeData.append(data)
    for l in l2:
        data = {}
        data['timestamp'] = l['timestamp']
        data['price'] = l['price']
        data['date'] = createDate(l['timestamp'])
        wholeData.append(data)
    return wholeData

def createTitle(_type, symbol, name):
    if _type == 'STOCK':
        return symbolLookup.stock_getNameFromSymbol(symbol, name)
    if _type == 'FOREX':
        return symbolLookup.forex_getNameFromSymbol(symbol)
    if _type == 'CRYPTO':
        return symbol.capitalize()

def createDate(timestamp):
    months = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}
    date = datetime.fromtimestamp(timestamp)
    return months[date.month].capitalize() + ' ' + str(date.day)

if __name__ == "__main__":
    #print(createDate(1586124000))
    print(create_graph('usd dkk', 'FOREX'))
    #print(json)
    #print(convertToDate(1589061600))