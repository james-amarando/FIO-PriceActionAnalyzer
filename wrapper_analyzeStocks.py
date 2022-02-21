import trendUtil
import priceUtil
import plotUtil
import time
import os

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


def checkMultiple(stocksToCheck, num_days=10):
    for ticker in stocksToCheck:
        time.sleep(1)
        print("\nChecking: "+ticker+" ("+str(num_days)+" day window)")
        checkSingle(
            ticker = ticker, 
            num_days = num_days, 
            alert_period = 3 , 
            alert_sigma_thresh = 1, 
            alert_num_instances_thresh = 1, 
            price_measure_to_use = "Close"
            )  
    return


def main():
    ticker = "ACN"
    num_days = 10
    alert_period = 3
    alert_sigma_thresh = 2
    alert_num_instances_thresh = 1
    price_measure_to_use = "Close"

    stockPrices = priceUtil.getPriceData(
        ticker = ticker, 
        num_days = num_days
        )

    print(stockPrices)
    print(stockPrices.keys())
    print("\n\nINDEX????")
    for d in stockPrices.index:
        date_str= d.strftime("%Y-%m-%d")

    print("\n\n")
    a = stockPrices.to_csv()
    print(a[0])
    print()

    stockPricesForAnalysis = []
    for p in stockPrices[price_measure_to_use]:
        stockPricesForAnalysis.append(p)
    stockPricesForAnalysis = np.asarray(stockPricesForAnalysis)

    stockDatesForAnalysis = []
    for d in stockPrices.index:
        stockDatesForAnalysis.append(d.strftime("%Y-%m-%d"))
    print(stockDatesForAnalysis)
    stockDatesForAnalysis = np.asarray(stockDatesForAnalysis)

    stockAnalysis = trendUtil.analyzeStockPricesV1(
        stockPrices = stockPricesForAnalysis, 
        alert_period = alert_period, 
        alert_sigma_thresh = alert_sigma_thresh, 
        alert_num_instances_thresh = alert_num_instances_thresh
        )

    plotUtil.createPlot(
        ticker = ticker, 
        stock_prices_dates = stockDatesForAnalysis, 
        stock_prices_vals = stockAnalysis["stockPrices"], 
        regression_line_dates = stockDatesForAnalysis, 
        regression_line_vals = stockAnalysis["regressionLine"], 
        sigma = stockAnalysis["sigma"], 
        num_sigmas = 3, 
        plot_title = ticker + ": (ten day window), Alert: "+str(stockAnalysis["alert"]),
        filename = ticker+"tenDay.png")

    return

if __name__ == "__main__":
    #main()
    stocksToCheck=["ACN","MSFT","F","BABA","AMZN","CTAS","BABA","CRM","FB","CRWD"]
    stocksToCheck += ["COIN","PLTR","Z","AAPL","GOOGL","TSLA","NVDA","JPM","JNJ","PG"]
    stocksToCheck += ["V","HD","BAC","XOM","MA","DIS","PFE","KO","AVGO","COST"]
    stocksToCheck += ["PEP","VZ","T","AMD","QCOM","MCD","INTC","UPS","NFLX","RTX"]
    stocksToCheck += ["ORCL","TMUS","GM","NOC","FDX","WM","CMG","CMCSA","EA","GE"]
    stocksToCheck += ["YUM","AAL","TAP"]
    checkMultiple(stocksToCheck,num_days=10)
    checkMultiple(stocksToCheck,num_days=20)
    checkMultiple(stocksToCheck,num_days=40)