import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn import metrics
import crypto_webscraper
import stock_webscraper

def do_lr_prediction(ClosePrices):
    df = pd.DataFrame(ClosePrices[::-1])
    forecast_out = 30
    df['Prediction'] = df.shift(-forecast_out)
    ### Create the independent data set (X)  #######
    # Convert the dataframe to a numpy array
    X = np.array(df.drop(['Prediction'], 1))

    # Remove the last 'n' rows
    X = X[:-forecast_out]

    ### Create the dependent data set (y)  #####
    # Convert the dataframe to a numpy array (All of the values including the NaN's)
    y = np.array(df['Prediction'])
    # Get all of the y values except the last 'n' rows
    y = y[:-forecast_out]
    # Split the data into 80% training and 20% testing
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    # Create and train the Linear Regression  Model
    lr = LinearRegression()
    # Train the model
    lr.fit(x_train, y_train)
    # Testing Model: Score returns the coefficient of determination R^2 of the prediction.
    # The best possible score is 1.0
    lr_confidence = lr.score(x_test, y_test)
    #print("lr confidence: ", lr_confidence)

    # Set x_forecast equal to the last 30 rows of the original data set from Adj. Close column
    prediction_forecast = np.array(df.drop(['Prediction'], 1))[-forecast_out:]
    # print(x_forecast)

    # Print linear regression model predictions for the next 'n' days
    lr_prediction = lr.predict(prediction_forecast)

    prediction_confidence = lr_confidence
    prediction = list(lr_prediction)
    return prediction, prediction_confidence

def lr_predict_improved(prices):
    dataset = pd.DataFrame(prices)
    x = dataset[['high', 'low', 'open']].values
    y = dataset['close'].values

    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=0)
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    #print(lr.coef_)
    #print(lr.intercept_)
    predicted = lr.predict(x_test)
    df = pd.DataFrame({'Actual':y_test.flatten(), 'Predicted':predicted.flatten()})
    df.to_csv('test.csv')

def predict_test(prices):
    prices = prices[::-1]
    df = pd.DataFrame(prices)
    forecast = 40
    df['Prediction'] = df[['Close']].shift(-forecast)
    x = np.array(df.drop(['Prediction', 'Date'],1))
    x = x[:-forecast]
    y = np.array(df['Prediction'])
    y = y[:-forecast]
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=1)
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.00009)
    svr_rbf.fit(x_train, y_train)
    svm_conf = svr_rbf.score(x_test, y_test)
    
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    #lr.fit(x_train, y_train)
    lr_conf = lr.score(x_test, y_test)
    print(svm_conf, lr_conf)

    x_forecast = np.array(df.drop(['Prediction', 'Date'],1))[-forecast:]
    lr_prediction = lr.predict(x_forecast)
    #print(lr_prediction)

    svm_prediction = svr_rbf.predict(x_forecast)
    #print(svm_prediction)
    if svm_conf > lr_conf:
        return svm_prediction, svm_conf, 'Support Vector Model'
    else:
        return lr_prediction, lr_conf, 'Linear Regression'

if __name__ == "__main__":
    #ClosePrices, DataPoints = crypto_webscraper.do_scrape('bitcoin')
    #do_lr_prediction(ClosePrices)
    #print(DataPoints[10:])
    #prices = crypto_webscraper.collectData('bitcoin')
    #lr_predict_improved(prices)
    prices = stock_webscraper.downloadCSV()
    print(predict_test(prices))