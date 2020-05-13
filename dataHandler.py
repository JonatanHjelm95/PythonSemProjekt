import crypto_webscraper
import Predict
from datetime import datetime, timedelta
import time



def getPriceData(stockType, name):
    if str(stockType) == 'STOCK':
        pass
    if str(stockType) == 'CRYPTO':
        return crypto_createFormattedData(name)
    if str(stockType) == 'FOREX':
        pass



### Shared Functions ###
def combineLatestData(latestDataPoints):
    latestData = []
    for i in range(len(latestDataPoints)):
        data = {}
        month, day, year = splitDateString(latestDataPoints[i]['date'])
        ts = createTimestamp(m=month, d=day, y=year)
        data['timestamp'] = ts
        data['price'] = latestDataPoints[i]['close']
        latestData.append(data)
    return latestData

def combinePredictionData(futureTimestamps, predictions):
    PredictionData = []
    for i in range(len(futureTimestamps)):
        prediction = {}
        prediction['timestamp'] = futureTimestamps[i]
        prediction['price'] = round(float(predictions[i]),2)
        PredictionData.append(prediction)
    return PredictionData

def splitDateString(date):
    dateSplit = str(date).split(' ')
    month = getMonth(dateSplit[0])
    return month, dateSplit[1], dateSplit[2]

def getMonth(m):
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    for i in range(len(months)):
        if str(m).lower() == months[i]:
            return i+1

def createTimestamp(m, d, y):
    dt = datetime(year=int(y), month=int(m), day=int(d))
    return int(time.mktime(dt.timetuple()))

def createFutureTimestamp(ts, n):
    date = datetime.fromtimestamp(ts)
    fdate = date + timedelta(days=n)
    return int(time.mktime(fdate.timetuple()))


### Crypto Functions ###
def crypto_createFormattedData(name):
    ClosePrices = getCryptoData(name)
    predictions, confidence, predictionMethod = Predict.predict_test(ClosePrices)
    latestDataPoints = crypto_getLatestDataPoints(ClosePrices)
    futureTimestamps = crypto_createFutureDates(latestDataPoints, predictions)
    PredictionData = combinePredictionData(futureTimestamps, predictions)
    latestData = combineLatestData(latestDataPoints)
    print(latestData, '||',  PredictionData)
    return latestData, PredictionData, confidence, predictionMethod

def getCryptoData(name):
    return crypto_webscraper.do_scrape(name)

# returning latest 30 days
def crypto_getLatestDataPoints(DataPoints):
    latestDataPoints = DataPoints[0:30]
    return latestDataPoints[::-1]

# Future dates for crypto; Every day
def crypto_createFutureDates(latestDataPoints, predictions):
    futureTimestamps = []
    for i in range(len(latestDataPoints)):
        month, day, year = splitDateString(latestDataPoints[i]['date'])
        ts = createTimestamp(m=month, d=day, y=year)
        fts = createFutureTimestamp(ts=ts, n=i+1)
        futureTimestamps.append(fts)
    return futureTimestamps

### Stock Functions ###
def getStockData(name):
    pass

# returning latest 30 days
def stock_getLatestDataPoints(DataPoints):
    latestDataPoints = DataPoints[0:30]
    return latestDataPoints[::-1]

# Future dates for stocks; only workdays
def stock_createFutureDates():
    pass

### Forex Functions ###
def getForexData(name):
    return crypto_webscraper.do_scrape(name)

# returning latest 30 days
def forex_getLatestDataPoints(DataPoints):
    latestDataPoints = DataPoints[0:30]
    return latestDataPoints[::-1]

# Future dates for forex; only workdays
def forex_createFutureDates():
    pass

if __name__ == "__main__":
    getPriceData('CRYPTO', 'bitcoin')