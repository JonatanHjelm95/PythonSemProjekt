import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn import metrics
import crypto_webscraper
import stock_webscraper

def predict(prices):
    # Reversing array
    prices = prices[::-1] 
    # Creating dataframe
    df = pd.DataFrame(prices)
    # Removing rows with null-values
    df.dropna(how='any',axis=0)
    df[df.Close != 'null']
    # Setting prediction-size
    forecast = 30
    # Creating Prediction column with prediction-size as offset
    df['Prediction'] = df[['Close']].shift(-forecast)
    # Setting x and y
    x = np.array(df.drop(['Prediction', 'Date'],1))
    x = x[:-forecast]
    y = np.array(df['Prediction'])
    y = y[:-forecast]
    # Training model with 20% test data
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=1)
    # Setting options on Support Vector Regression
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma='scale')
    # Doing SVR fit with training data
    svr_rbf.fit(x_train, y_train)
    svm_conf = svr_rbf.score(x_test, y_test)
    # Creating Linear Regression object
    lr = LinearRegression()
    # Doing LR fit with training data
    lr.fit(x_train, y_train)
    lr_conf = lr.score(x_test, y_test)
    # Creating np-array with prediction data
    x_forecast = np.array(df.drop(['Prediction', 'Date'],1))[-forecast:]
    # Creating predictions
    lr_prediction = lr.predict(x_forecast)
    svm_prediction = svr_rbf.predict(x_forecast)
    # Returns prediction with highest conf
    if svm_conf > lr_conf:
        return svm_prediction, svm_conf, 'Support Vector Regression'
    else:
        return lr_prediction, lr_conf, 'Linear Regression'

def predict_specific(prices, _type, n, gamma, kernel):
    n = int(n)
    # Setting minimum prediction size=30
    if n < 30:
        n = 30
    # Parsing gamma as float if contains digit
    if ',' in str(gamma):
        gamma.replace(',','.')
    if str(gamma).replace('.','').isdigit():
        # Setting max gamma value=1.0
        if float(gamma) > 1:
            gamma = 1.0
        else:
            gamma = float(gamma)
    
    # Reversing array
    prices = prices[::-1] 
    # Creating dataframe
    df = pd.DataFrame(prices)
    # Removing rows with null-values
    df.dropna(how='any',axis=0)
    df[df.Close != 'null']
    # Setting prediction-size
    forecast = n
    # Creating Prediction column with prediction-size as offset
    df['Prediction'] = df[['Close']].shift(-forecast)
    # Setting x and y
    x = np.array(df.drop(['Prediction', 'Date'],1))
    x = x[:-forecast]
    y = np.array(df['Prediction'])
    y = y[:-forecast]
    # Training model with 20% test data
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=1)
    # Setting options on Support Vector Regression
    svr_rbf = SVR(kernel=kernel, C=1e3, gamma=gamma)
    # Doing SVR fit with training data
    svr_rbf.fit(x_train, y_train)
    svm_conf = svr_rbf.score(x_test, y_test)
    # Creating Linear Regression object
    lr = LinearRegression()
    # Doing LR fit with training data
    lr.fit(x_train, y_train)
    lr_conf = lr.score(x_test, y_test)
    # Creating np-array with prediction data
    x_forecast = np.array(df.drop(['Prediction', 'Date'],1))[-forecast:]
    # Creating predictions
    lr_prediction = lr.predict(x_forecast)
    svm_prediction = svr_rbf.predict(x_forecast)

    if _type == 'SVM':
        return svm_prediction, svm_conf, 'Support Vector Regression'
    else:
        return lr_prediction, lr_conf, 'Linear Regression'


if __name__ == "__main__":
    string = '1.23'
    print(string.replace('.','').isdigit())
