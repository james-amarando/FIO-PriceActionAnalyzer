import trendUtil
import priceUtil
import plotUtil
import datetime

import numpy as np

def main():
    ticker = "ACN"
    num_days = 10
    alert_period = 3
    alert_sigma_thresh = 3
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
        plot_title_info="Ten Day")

    return

if __name__ == "__main__":
    main()