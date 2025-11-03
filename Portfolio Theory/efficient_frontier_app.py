
import numpy as np
import datetime as dt
import yfinance as yf

def getData(stocks, start_date, end_date):
    stockData = yf.download(stocks, start=start_date, end=end_date)
    stockData = stockData['Close']

    returns = stockData.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()

    return meanReturns, covMatrix


def portfolioPerformance(weights, meanReturns, covMatrix):
    returns = np.sum(meanReturns*weights)*252
    std = np.sqrt(np.dot(weights.T, np.dot(covMatrix, weights))) * np.sqrt(252)
    return returns, std


stockList = ['CBA', 'BHP', 'TLS']
stocks = [stock+'.AX' for stock in stockList] # On the Austrualian Stock Exchange

endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=365)
weights = np.array([0.3, 0.3, 0.4])

#print(getData(stocks=stocks, start_date=startDate, end_date=endDate))
meanReturns, covMatrix = getData(stocks=stocks, start_date=startDate, end_date=endDate)
returns, std = portfolioPerformance(weights=weights, meanReturns=meanReturns, covMatrix=covMatrix)

print(f'Portfoliot Returns: {round(returns*100, 2)}\nSTD of Porfolio: {round(std, 2)}')