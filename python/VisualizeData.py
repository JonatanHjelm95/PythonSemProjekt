import matplotlib.pyplot as plt, mpld3
import dataHandler
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import symbolLookup
import os.path
import io
import base64
import json

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
        print(currentTimestamp)
        # defining plotsize
        plt.subplots(figsize=(20,5))
        # plotting all data
        plt.plot(df['date'], df['price'], 'ks-', c = 'blue', label='Historical prices')
        # plotting prediction data on top
        plt.plot(df[df.timestamp >= currentTimestamp]['date'], df[df.timestamp >= currentTimestamp]['price'], 'ks-', c = 'red', label='Predicted prices')
        # Setting title, methods and Coef
        title = createTitle(_type, title, name)
        plt.title(title + ', ' + str(method) +', Confidence: '+ str(round(float(confidence),2)))
        # Rotating x labels
        plt.xticks(rotation = 45)
        # Setting grrid
        plt.grid()
        #plt.show()
        # Converting plot to png and encoding as base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        pic_hash = base64.b64encode(buf.read())
        # Creating json response
        jsonDict = {}
        jsonDict['title'] = title
        jsonDict['method'] = str(method)
        jsonDict['coef'] = str(confidence)
        jsonDict['prices'] = list(df['price'])
        jsonDict['dates'] = list(df['date'])
        jsonDict['graph'] = str(pic_hash)
        
        return json.dumps(jsonDict)
    except Exception as e:
        jsonDict = {}
        if str(e) == "'DataFrame' object has no attribute 'Close'":
            jsonDict['error'] = _type.lower() + ' does not exist'
        else:
            jsonDict['error'] = str(e)
        return json.dumps(jsonDict)


    
    

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
    print(create_graph('google', 'STOCK'))
    #print(json)
    #print(convertToDate(1589061600))