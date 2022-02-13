import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def calculateRegressionLine(stockPrices):
    x = np.arange(0, len(stockPrices), 1, dtype=int)
    x_next_10 = np.arange(len(stockPrices)-1, len(stockPrices)+9, 1, dtype=int)
    y = stockPrices
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    regressionLine = {}
    regressionLine["gradient"] = gradient
    regressionLine["intercept"] = intercept
    regressionLine["rValue"] = r_value
    regressionLine["pValue"] = p_value
    regressionLine["points"] = regressionLine["gradient"]*x+regressionLine["intercept"]
    regressionLine["pointsNext10"] = regressionLine["gradient"]*x_next_10+regressionLine["intercept"]
    return regressionLine


def calculateSigmaDistances(stockPrices, sigma):

    return


def createPlot10Days(stockPricesLastTen, regressionLineLastTen, stockPricesPrevLastTen, regressionLinePrevLastTen, sigma_last_ten, sigma_prev_last_ten, stock_name):
    # Config items
    num_sigmas = 3
    
    # Create x axis variables
    days_last_10 = np.arange(-10, 0, 1, dtype=int)
    days_prev_last_10 = np.arange(-20, -10, 1, dtype=int)
    days_next_10 = np.arange(days_last_10[-1], days_last_10[-1]+10, 1, dtype=int)

    # Init figure
    plt.figure(figsize=(12, 4))
   
    # plot last 20 days of stock price
    daysLast20 = np.concatenate((days_prev_last_10,days_last_10))
    stockPricesLast20 = np.concatenate((stockPricesPrevLastTen,stockPricesLastTen))
    plt.plot(daysLast20, stockPricesLast20, '.-',c="r") 

    # Plot last 10 regression line, and sigma lines
    plt.plot(days_last_10, regressionLineLastTen["points"],"k")
    for i in range(1,num_sigmas+1):
        plt.plot(days_last_10, regressionLineLastTen["points"]+i*sigma_last_ten,"--k")
        plt.plot(days_last_10, regressionLineLastTen["points"]-i*sigma_last_ten,"--k")

    # Plot previous last ten regression line, and sigma lines
    plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"],"0.8")
    for i in range(1,num_sigmas+1):
        plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"]+i*sigma_prev_last_ten,"--",c="0.8")
        plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"]-i*sigma_prev_last_ten,"--",c="0.8")
    
    # Projecting the trend lines ahead
    plt.plot(days_next_10, regressionLineLastTen["pointsNext10"],"y")
    for i in range(1,num_sigmas+1):
        plt.plot(days_next_10, regressionLineLastTen["pointsNext10"]+i*sigma_last_ten,"--y")
        plt.plot(days_next_10, regressionLineLastTen["pointsNext10"]-i*sigma_last_ten,"--y")
 

    plt.title(stock_name+": Ten Day Window View")
    plt.ylabel("Stock Price ($)")
    plt.xlabel("Days")
    plt.savefig(stock_name+"_tenDay.png")
    plt.show()
    return


def createPlot20Days(stockPricesLastTen, stockPricesPrevLastTen, regressionLineLastTwenty, sigma_last_twenty, stock_name):
    # Config items
    num_sigmas = 3
    
    # Create x axis variables
    days_last_10 = np.arange(-10, 0, 1, dtype=int)
    days_prev_last_10 = np.arange(-20, -10, 1, dtype=int)
    daysLast20 = np.concatenate((days_prev_last_10,days_last_10))
    daysNext10 = np.arange(days_last_10[-1], days_last_10[-1]+10, 1, dtype=int)

    # Init figure
    plt.figure(figsize=(12, 4))
   
    # plot last 20 days of stock price
    stockPricesLast20 = np.concatenate((stockPricesPrevLastTen,stockPricesLastTen))
    plt.plot(daysLast20, stockPricesLast20, '.-',c="r") 

    # last 20 days of regression lines
    plt.plot(daysLast20, regressionLineLastTwenty["points"],"k")
    for i in range(1,num_sigmas+1): 
        plt.plot(daysLast20, regressionLineLastTwenty["points"]+i*sigma_last_twenty,"--k")
        plt.plot(daysLast20, regressionLineLastTwenty["points"]-i*sigma_last_twenty,"--k")

    # Next 10 day projection
    plt.plot(daysNext10, regressionLineLastTwenty["pointsNext10"],"y")
    for i in range(1,num_sigmas+1):
        plt.plot(daysNext10, regressionLineLastTwenty["pointsNext10"]+i*sigma_last_twenty,"--y")
        plt.plot(daysNext10, regressionLineLastTwenty["pointsNext10"]-i*sigma_last_twenty,"--y")
 

    plt.title(stock_name+": Twenty Day Window View")
    plt.ylabel("Stock Price ($)")
    plt.xlabel("Days")
    plt.savefig(stock_name+"_twentyDay.png")
    plt.show()
    return


def main():
    stock_name = "AMA"
    stockPricesLastTwenty = np.array([99, 98, 99, 99, 100, 101, 102, 101, 102, 100, 102,103,102,106,105,106,107,107,105,109])
    stockPricesNextTen = np.array([109,109,111,111,110,113,112,113,114,112])

    stock_name = "ACN"
    stockPricesLastTwenty = np.array([353, 348, 344, 343, 336, 339, 335, 330, 333, 343, 354, 353, 359, 346, 348, 344, 345, 356, 342, 329])
    stockPricesNextTen = np.array([109,109,111,111,110,113,112,113,114,112])

    # Group prices 
    stockPricesPrevLastTen = stockPricesLastTwenty[0:10]
    stockPricesLastTen = stockPricesLastTwenty[-10:]
    #print(stockPricesPrevLastTen)
    #print(stockPricesLastTen)

    # Calculate values
    regressionLineLastTen = calculateRegressionLine(stockPricesLastTen)
    sigma_last_ten = np.std(stockPricesLastTen - regressionLineLastTen["points"])
    sigmaDistancesLastTen = calculateSigmaDistances(stockPricesLastTen, sigma_last_ten)

    regressionLinePrevLastTen = calculateRegressionLine(stockPricesPrevLastTen)
    sigma_prev_last_ten = np.std(stockPricesPrevLastTen - regressionLinePrevLastTen["points"])
    sigmaDistancesPrevLastTen = calculateSigmaDistances(stockPricesPrevLastTen, sigma_prev_last_ten)

    regressionLineLastTwenty = calculateRegressionLine(stockPricesLastTwenty)
    sigma_last_twenty = np.std(stockPricesLastTwenty - regressionLineLastTwenty["points"])
    sigmaDistancesLastTwenty = calculateSigmaDistances(stockPricesLastTwenty, sigma_last_twenty)
    
    # Now plot
    createPlot10Days(stockPricesLastTen, regressionLineLastTen, stockPricesPrevLastTen, regressionLinePrevLastTen, sigma_last_ten, sigma_prev_last_ten, stock_name)
    createPlot20Days(stockPricesLastTen, stockPricesPrevLastTen, regressionLineLastTwenty, sigma_last_twenty, stock_name)
    '''
    days_last_20 = np.arange(0, len(stockPricesLastTwenty), 1, dtype=int)
    days_last_10 = np.arange(10, 20, 1, dtype=int)
    days_prev_last_10 = np.arange(0, 10, 1, dtype=int)
    days_next_10 = np.arange(days_last_10[-1], days_last_10[-1]+10, 1, dtype=int)

    #plt.plot(days_last_20, stockPricesLastTwenty, 'or') 

  
    plt.plot(days_last_10, stockPricesLastTen, 'ok') 
    plt.plot(days_last_10, regressionLineLastTen["points"],"k")
    plt.plot(days_last_10, regressionLineLastTen["points"]+sigma_last_ten,"--k")
    plt.plot(days_last_10, regressionLineLastTen["points"]+2*sigma_last_ten,"--k")
    plt.plot(days_last_10, regressionLineLastTen["points"]+3*sigma_last_ten,"--k")
    plt.plot(days_last_10, regressionLineLastTen["points"]-sigma_last_ten,"--k")
    plt.plot(days_last_10, regressionLineLastTen["points"]-2*sigma_last_ten,"--k")
    plt.plot(days_last_10, regressionLineLastTen["points"]-3*sigma_last_ten,"--k")
    
    plt.plot(days_prev_last_10, stockPricesPrevLastTen, 'ob') 
    plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"],"b")
    plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"]+sigma_prev_last_ten,"--b")
    plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"]+2*sigma_prev_last_ten,"--b")
    plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"]+3*sigma_prev_last_ten,"--b")
    plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"]-sigma_prev_last_ten,"--b")
    plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"]-2*sigma_prev_last_ten,"--b")
    plt.plot(days_prev_last_10, regressionLinePrevLastTen["points"]-3*sigma_prev_last_ten,"--b")

    plt.plot(days_last_20, regressionLineLastTwenty["points"],"y")
    plt.plot(days_last_20, regressionLineLastTwenty["points"]+sigma_last_twenty,"--y")
    plt.plot(days_last_20, regressionLineLastTwenty["points"]+2*sigma_last_twenty,"--y")
    plt.plot(days_last_20, regressionLineLastTwenty["points"]+3*sigma_last_twenty,"--y")
    plt.plot(days_last_20, regressionLineLastTwenty["points"]-sigma_last_twenty,"--y")
    plt.plot(days_last_20, regressionLineLastTwenty["points"]-2*sigma_last_twenty,"--y")
    plt.plot(days_last_20, regressionLineLastTwenty["points"]-3*sigma_last_twenty,"--y")

    # Projecting ahead
    plt.plot(days_next_10, regressionLineLastTen["pointsNext10"],"k")
    plt.plot(days_next_10, regressionLineLastTen["pointsNext10"]+sigma_last_ten,"--k")
    plt.plot(days_next_10, regressionLineLastTen["pointsNext10"]+2*sigma_last_ten,"--k")
    plt.plot(days_next_10, regressionLineLastTen["pointsNext10"]+3*sigma_last_ten,"--k")
    plt.plot(days_next_10, regressionLineLastTen["pointsNext10"]-sigma_last_ten,"--k")
    plt.plot(days_next_10, regressionLineLastTen["pointsNext10"]-2*sigma_last_ten,"--k")
    plt.plot(days_next_10, regressionLineLastTen["pointsNext10"]-3*sigma_last_ten,"--k")

    
    plt.plot(days_next_10, regressionLineLastTwenty["pointsNext10"],"y")
    plt.plot(days_next_10, regressionLineLastTwenty["pointsNext10"]+sigma_last_twenty,"--y")
    plt.plot(days_next_10, regressionLineLastTwenty["pointsNext10"]+2*sigma_last_twenty,"--y")
    plt.plot(days_next_10, regressionLineLastTwenty["pointsNext10"]+3*sigma_last_twenty,"--y")
    plt.plot(days_next_10, regressionLineLastTwenty["pointsNext10"]-sigma_last_twenty,"--y")
    plt.plot(days_next_10, regressionLineLastTwenty["pointsNext10"]-2*sigma_last_twenty,"--y")
    plt.plot(days_next_10, regressionLineLastTwenty["pointsNext10"]-3*sigma_last_twenty,"--y")

    plt.show()
    '''

    return

if __name__ == "__main__":
    main()