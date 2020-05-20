# Python Semester Projekt

# Stock Predictions
- This project focuses on producing a 30 day close price prediction on any stock, foreign valuta or cryptocurrency.

- Input will be given with a POST-request to a remote FLASK-server, and outputted as an array and a graph

- Price data will be collected with webscraping, and predictions will be produced through SKLearn, using Linear Regression and SVM (Support Vector Machines)

NOTE: Predictions is based solely on Linear Regression and SVM from historical price data, and should not be used to make investment decisions.
This is only used to demontrate some of the features of SKLearn.
More data = higher Coef/Confidence.


# Techs
- Pandas
- MatPlotLib
- Requests
- Numpy
- Websraping
- Flask
- Machine Learning (SKLearn)

# Challenges
The biggest challenge was to get the right stock/forex/crypto symbol from user input.
This took a while to fix, but was eventually solved using even more webscraping.
The end results is quite good, and performing a search is pretty easy

# How to run
- Open python folder, run flaskApp.py; Make post requests to localhost:5001/api/predict
with jsonbody { "name": "some name", "type": "STOCK/FOREX/CRYPTO" }
- try demo at: http://167.172.164.163/
