
import matplotlib.pyplot as plt


def createPlot(ticker, stock_prices_dates, stock_prices_vals, regression_line_dates, regression_line_vals, sigma, plot_title, filename, num_sigmas=3, show=False):
    
    plt.figure(figsize=(12,4))

    # Plot stock price
    plt.plot(stock_prices_dates, stock_prices_vals, ".-", c="r")

    # Plot regression line
    plt.plot(regression_line_dates, regression_line_vals, "k")

    # Plot the sigmas
    for i in range(1, num_sigmas+1):
        plt.plot(regression_line_dates, regression_line_vals+i*sigma, "--k")
        plt.plot(regression_line_dates, regression_line_vals-i*sigma, "--k")

    plt.title(plot_title)
    plt.ylabel("Stock Price ($)")
    plt.xlabel("Date")
    plt.savefig(filename)
    if show:
        plt.show()
    plt.close()

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


def main():
    return

if __name__ == "__main__":
    main()