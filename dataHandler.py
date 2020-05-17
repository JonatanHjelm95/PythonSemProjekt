import crypto_webscraper
import stock_webscraper
import Predict
from datetime import datetime, timedelta
import time



def getPriceData(_type, name):
    if str(_type) == 'STOCK':
        return stock_createFormattedData(name)
    if str(_type) == 'CRYPTO':
        return crypto_createFormattedData(name)
    if str(_type) == 'FOREX':
        pass



### Shared Functions ###


def combinePredictionData(futureTimestamps, predictions):
    PredictionData = []
    for i in range(len(futureTimestamps)):
        prediction = {}
        prediction['timestamp'] = futureTimestamps[i]
        prediction['price'] = round(float(predictions[i]),2)
        PredictionData.append(prediction)
    return PredictionData

def crypto_splitDateString(date):
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

def createFutureTimestamp_weekday(ts, n):
    date = datetime.fromtimestamp(ts)
    fdate = date + timedelta(days=n)
    if fdate.weekday() < 5:
        return int(time.mktime(fdate.timetuple()))
    else:
        fdate = fdate + timedelta(days=1)
        if fdate.weekday() < 5:
            return int(time.mktime(fdate.timetuple()))
        else:
            fdate = fdate + timedelta(days=1)
            return int(time.mktime(fdate.timetuple()))



def getLatestDataPoints(DataPoints):
    latestDataPoints = DataPoints[0:30]
    return latestDataPoints[::-1]
########################
### Crypto Functions ###
########################
def crypto_createFormattedData(name):
    ClosePrices = getCryptoData(name)
    predictions, confidence, predictionMethod = Predict.predict_test(ClosePrices)
    latestDataPoints = getLatestDataPoints(ClosePrices)
    futureTimestamps = crypto_createFutureDates(latestDataPoints, predictions)
    PredictionData = combinePredictionData(futureTimestamps, predictions)
    latestData = crypto_combineLatestData(latestDataPoints)
    return latestData, PredictionData, confidence, predictionMethod

def getCryptoData(name):
    return crypto_webscraper.do_scrape(name)

def crypto_combineLatestData(latestDataPoints):
    latestData = []
    for i in range(len(latestDataPoints)):
        data = {}
        month, day, year = crypto_splitDateString(latestDataPoints[i]['Date'])
        ts = createTimestamp(m=month, d=day, y=year)
        data['timestamp'] = ts
        data['price'] = latestDataPoints[i]['Close']
        latestData.append(data)
    return latestData

# Future dates for crypto; Every day
def crypto_createFutureDates(latestDataPoints, predictions):
    futureTimestamps = []
    month, day, year = crypto_splitDateString(latestDataPoints[-1]['Date'])
    ts = createTimestamp(m=month, d=day, y=year)
    for i in range(len(latestDataPoints)):   
        fts = createFutureTimestamp(ts=ts, n=i+1)
        futureTimestamps.append(fts)
    return futureTimestamps
#######################
### Stock Functions ###
#######################
def stock_createFormattedData(name):
    ClosePrices = stock_webscraper.downloadCSV(name)
    predictions, confidence, predictionMethod = Predict.predict_test(ClosePrices)
    latestDataPoints = stock_getLatestDataPoints(ClosePrices)
    futureTimestamps = stock_createFutureDates(latestDataPoints, predictions)
    PredictionData = combinePredictionData(futureTimestamps, predictions)
    latestData = stock_combineLatestData(latestDataPoints)
    return latestData, PredictionData, confidence, predictionMethod
    #return predictions

def stock_splitDateString(date):
    dateSplit = str(date).split('-')
    return int(dateSplit[1]), int(dateSplit[2]), int(dateSplit[0])

def stock_combineLatestData(latestDataPoints):
    latestData = []
    dates = list(latestDataPoints['Date'])
    prices = list(latestDataPoints['Close'])
    for i in range(len(dates)):
        data = {}
        month, day, year = stock_splitDateString(str(dates[i]))
        ts = createTimestamp(m=month, d=day, y=year)
        data['timestamp'] = ts
        data['price'] = prices[i]
        latestData.append(data)
    return latestData

# returning latest 30 days
def stock_getLatestDataPoints(DataPoints):
    latestDataPoints = DataPoints[0:30]
    return latestDataPoints[::-1]

# Future dates for stocks; only weekdays
def stock_createFutureDates(latestDataPoints, predictions):
    futureTimestamps = []
    dates = list(latestDataPoints['Date'])
    latestDate = str(dates[-1])
    month, day, year = stock_splitDateString(latestDate)
    ts = createTimestamp(m=month, d=day, y=year)
    for i in range(len(latestDataPoints)):
        fts = createFutureTimestamp_weekday(ts=ts, n=1)
        futureTimestamps.append(fts)
        ts = fts
    return futureTimestamps

#######################
### Forex Functions ###
#######################
def getForexData(name):
    return crypto_webscraper.do_scrape(name)

# returning latest 30 days
def forex_getLatestDataPoints(DataPoints):
    latestDataPoints = DataPoints[0:30]
    return latestDataPoints[::-1]

# Future dates for forex; only workdays
def forex_createFutureDates(latestDataPoints, predictions):

    pass

### Test functions ###

def tsToDate(ts):
    print(datetime.fromtimestamp(ts))

if __name__ == "__main__":
    print(stock_createFormattedData('novo nordisk'))
    #getPriceData('CRYPTO', 'bitcoin')