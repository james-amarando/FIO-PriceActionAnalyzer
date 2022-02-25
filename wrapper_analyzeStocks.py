import trendUtil
import priceUtil
import plotUtil
import datetime
import os
import tickerUtil   

import numpy as np



def checkSingle(ticker, num_days, alert_period=3, alert_sigma_thresh=2, alert_num_instances_thresh=1, price_measure_to_use="Close"):
    
    stockPrices = priceUtil.getPriceData(
        ticker = ticker, 
        num_days = num_days
        )

    stockPricesForAnalysis = []
    for p in stockPrices[price_measure_to_use]:
        stockPricesForAnalysis.append(p)
    stockPricesForAnalysis = np.asarray(stockPricesForAnalysis)

    stockDatesForAnalysis = []
    for d in stockPrices.index:
        stockDatesForAnalysis.append(d.strftime("%Y-%m-%d"))
    stockDatesForAnalysis = np.asarray(stockDatesForAnalysis)

    stockAnalysis = trendUtil.analyzeStockPricesV1(
        stockPrices = stockPricesForAnalysis, 
        alert_period = alert_period, 
        alert_sigma_thresh = alert_sigma_thresh, 
        alert_num_instances_thresh = alert_num_instances_thresh
        )

    if stockAnalysis["alert"]:
        print("Alert for: "+ticker)
        plotUtil.createPlot(
            ticker = ticker, 
            stock_prices_dates = stockDatesForAnalysis, 
            stock_prices_vals = stockAnalysis["stockPrices"], 
            regression_line_dates = stockDatesForAnalysis, 
            regression_line_vals = stockAnalysis["regressionLine"], 
            sigma = stockAnalysis["sigma"], 
            num_sigmas = 3, 
            plot_title = ticker + ": ("+str(num_days)+" window), Alert: "+str(stockAnalysis["alert"]),
            filename = os.path.join("alerts",ticker+"_"+str(num_days)+"window.png")
            )
        alert = True
    else:
        alert = False
    return alert


def checkMultiple(stocksToCheck, num_days=10):
    stocksWithAlerts = []
    for ticker in stocksToCheck:
        print("\nChecking: "+ticker+" ("+str(num_days)+" day window)")
        alert = checkSingle(
            ticker = ticker, 
            num_days = num_days, 
            alert_period = 3 , 
            alert_sigma_thresh = 2, 
            alert_num_instances_thresh = 1, 
            price_measure_to_use = "Close"
            )
        if alert:
            stocksWithAlerts.append(ticker)  
    return stocksWithAlerts


def main():
    top100 = tickerUtil.getTop100Tickers()
    others = tickerUtil.getInterestingTickersNotTop100()
    stocksToCheck =  top100 + others

    tenDayAlerts = checkMultiple(stocksToCheck,num_days=10)
    twentyDayAlerts = checkMultiple(stocksToCheck,num_days=20)
    fourtyDayAlerts = checkMultiple(stocksToCheck,num_days=40)

    print("\n===========================")
    print("Analysis: "+datetime.datetime.today().strftime("%Y-%m-%d"))
    print("===========================")
    print("10 Day Regression Alerts:")
    print(tenDayAlerts)
    print("\n")
    print("20 Day Regression Alerts:")
    print(twentyDayAlerts)
    print("\n")
    print("40 Day Regression Alerts:")
    print(fourtyDayAlerts)
    print("\n")
    
    return

if __name__ == "__main__":
    main()