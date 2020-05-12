import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import crypto_webscraper

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
    x_forecast = np.array(df.drop(['Prediction'], 1))[-forecast_out:]
    # print(x_forecast)

    # Print linear regression model predictions for the next 'n' days
    lr_prediction = lr.predict(x_forecast)

    # Print support vector regressor model predictions for the next 'n' days
    print(lr_confidence)
    print(list(lr_prediction)[::-1])
    # print(svm_prediction)

if __name__ == "__main__":
    ClosePrices = crypto_webscraper.do_scrape('bitcoin')
    do_lr_prediction(ClosePrices)