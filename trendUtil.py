from math import dist
import numpy as np
from scipy import stats

def calculateRegressionLine(stockPrices):
    x = np.arange(0, len(stockPrices), 1, dtype=int)
    y = stockPrices
    print(x)
    print(y)
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    regressionLine = {}
    regressionLine["gradient"] = gradient
    regressionLine["intercept"] = intercept
    regressionLine["rValue"] = r_value
    regressionLine["pValue"] = p_value
    regressionLine["points"] = regressionLine["gradient"]*x+regressionLine["intercept"]
    return regressionLine

def analyzeStockPricesV1(stockPrices, alert_period=3, alert_sigma_thresh=2, alert_num_instances_thresh=1):
    '''
    IMPORTANT!!!
    This assumes stockPrices[0] is the OLDEST price and stockPrices[-1] is the MOST RECENT
    (i.e. list goes from oldest to newest)

    This will take a look at a set of stock prices and:
      1. Calculate regression line
      2. Analyze stddev of each point from that regression line
      3. Flag an alert if there are at least alert_num_instances in the most recent alert_period where |sigma_dist| >= alert_num_instances_thresh
    '''
    regressionLine = calculateRegressionLine(stockPrices)
    distancesFromRegression = stockPrices - regressionLine["points"]
    sigma = np.std(distancesFromRegression)
    sigmaDistances = distancesFromRegression / sigma

    alert_num_instances_meas = len([a for a in sigmaDistances[-alert_period:] if a > abs(alert_sigma_thresh)])
    if alert_num_instances_meas >= alert_num_instances_thresh:
        alert = True
    else:
        alert = False
    
    stockAnalysis = {}
    stockAnalysis["stockPrices"] = stockPrices
    stockAnalysis["regressionLine"] = regressionLine["points"]
    stockAnalysis["sigma"] = sigma
    stockAnalysis["distancesFromRegression"] = distancesFromRegression
    stockAnalysis["sigmaDistances"] = sigmaDistances
    stockAnalysis["alert_period"] = alert_period
    stockAnalysis["alert_sigma_thresh"] = alert_sigma_thresh
    stockAnalysis["alert_num_instances_thresh"] = alert_num_instances_thresh
    stockAnalysis["alert_num_instances_meas"] = alert_num_instances_meas
    stockAnalysis["alert"] = alert

    print(stockAnalysis)
    return stockAnalysis