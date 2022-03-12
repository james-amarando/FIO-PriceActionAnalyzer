import trendUtil
import priceUtil
import plotUtil
import datetime
import os
import tickerUtil   
import utils.googleSheetUtil as googleSheetUtil
import time

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


def checkMultiple(stocksToCheck, alert_period, alert_sigma_thresh, alert_num_instances_thresh, price_measure_to_use, num_days=10):
    stocksWithAlerts = []
    for ticker in stocksToCheck:
        print("\nChecking: "+ticker+" ("+str(num_days)+" day window)")
        alert = checkSingle(
            ticker = ticker, 
            num_days = num_days, 
            alert_period = alert_period , 
            alert_sigma_thresh = alert_sigma_thresh, 
            alert_num_instances_thresh = alert_num_instances_thresh, 
            price_measure_to_use = price_measure_to_use 
            )
        if alert:
            stocksWithAlerts.append(ticker)  
    return stocksWithAlerts

def reportToGoogleSheet(tenDayAlerts,twentyDayAlerts,fourtyDayAlerts,date_str,alert_period,alert_sigma_thresh,alert_num_instances_thresh):
    # Vars
    spreadsheet_id = "1bh_On-6hfOOBdGcRgbH5QV2iUgQx3nOXTYkS7NkLVV0"
    sheet_id = "1815780437"
    sheet_name = "Regression Analysis"

    # Logic
    sheet = googleSheetUtil.connectToGoogleSheet()
    googleSheetUtil.clearRowsRange(
        sheet = sheet,
        spreadsheet_id = spreadsheet_id,
        sheet_name = sheet_name,
        row_num_a = 1,
        row_num_b = 45
    )

    window_decriptor = "Last "+str(alert_period)+" day(s)"
    sigma_thresh_descriptor = str(alert_sigma_thresh)+" sigma"
    alert_occurance_thresh_descriptor = str(alert_num_instances_thresh)+" instance(s)"

    sheetRows = []
    sheetRows.append(["Date",date_str])
    sheetRows.append(["Window",window_decriptor])
    sheetRows.append(["Min Occurance",alert_occurance_thresh_descriptor])
    sheetRows.append(["Thresh",sigma_thresh_descriptor])
    sheetRows.append([""])
    sheetRows.append(["10 Day","20 Day","40 Day"])

    # I know there's an easier way to do this but I'm rushing to write this script quickly and can't look it up
    longest_alert = max(len(tenDayAlerts),len(twentyDayAlerts),len(fourtyDayAlerts))
    for i in range(0,longest_alert):
        if i < len(tenDayAlerts):
            ten_day =  tenDayAlerts[i]
        else:
            ten_day = ""

        if i < len(twentyDayAlerts):
            twenty_day =  twentyDayAlerts[i]
        else:
            twenty_day = ""

        if i < len(fourtyDayAlerts):
            fourty_day =  fourtyDayAlerts[i]
        else:
            fourty_day = ""

        sheetRows.append([ten_day,twenty_day,fourty_day])
    
    # Now write it
    for i in range(0,len(sheetRows)):
        row_num = i + 1  # Google isn't 0 indexed
        sheetRow = sheetRows[i]
        print("About to write row: "+str(sheetRow))
        googleSheetUtil.writeFullRow(
            sheet = sheet,
            spreadsheet_id = spreadsheet_id,
            sheet_name = sheet_name,
            row_num = row_num,
            row_content_list = sheetRow)
        time.sleep(1)

    return


def main():
    # configs
    alert_period = 1
    alert_sigma_thresh = 2
    alert_num_instances_thresh = 1
    price_measure_to_use = "Close"
    date_str = datetime.datetime.today().strftime("%Y-%m-%d")

    # Get tickets
    top100 = tickerUtil.getTop100Tickers()
    others = tickerUtil.getInterestingTickersNotTop100()
    stocksToCheck =  top100 + others

    # Clear directory of previous graphs
    alerts_dir = "alerts"
    for f in os.listdir(alerts_dir):
        os.remove(os.path.join(alerts_dir, f))
    
    # run analysis
    tenDayAlerts = checkMultiple(
        stocksToCheck = stocksToCheck, 
        alert_period = alert_period, 
        alert_sigma_thresh = alert_sigma_thresh, 
        alert_num_instances_thresh = alert_num_instances_thresh, 
        price_measure_to_use = price_measure_to_use, 
        num_days=10)

    twentyDayAlerts = checkMultiple(
        stocksToCheck = stocksToCheck, 
        alert_period = alert_period, 
        alert_sigma_thresh = alert_sigma_thresh, 
        alert_num_instances_thresh = alert_num_instances_thresh, 
        price_measure_to_use = price_measure_to_use, 
        num_days=20)

    fourtyDayAlerts = checkMultiple(
        stocksToCheck = stocksToCheck, 
        alert_period = alert_period, 
        alert_sigma_thresh = alert_sigma_thresh, 
        alert_num_instances_thresh = alert_num_instances_thresh, 
        price_measure_to_use = price_measure_to_use, 
        num_days=40)
    
    # Write To Google Sheet
    reportToGoogleSheet(
        tenDayAlerts = tenDayAlerts,
        twentyDayAlerts = twentyDayAlerts,
        fourtyDayAlerts = fourtyDayAlerts,
        date_str = date_str,
        alert_period = alert_period,
        alert_sigma_thresh = alert_sigma_thresh,
        alert_num_instances_thresh = alert_num_instances_thresh)

    # Print results to command line
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