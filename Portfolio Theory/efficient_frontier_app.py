
import numpy as np
import datetime as dt
import yfinance as yf
import scipy.optimize as sc

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


def negativeSR(weights, meanReturns, covMatrix, riksFreeRate = 0):
    pReturns, pStd = portfolioPerformance(weights=weights, meanReturns=meanReturns, covMatrix=covMatrix)
    return -(pReturns - riksFreeRate)/pStd


def maxSH(meanReturns, covMatrix, riskFreeRate=0, constraintSet=(0,1)):
    # Minimize the negative Sharpe Ratio (i.e. Maximising the Sharpe Ratio)
    # by adjusting the weights (how much we allocate to each asset)
    num_assets = len(meanReturns)
    args = (meanReturns, covMatrix, riskFreeRate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range(num_assets))
    results = sc.minimize(negativeSR, num_assets*[1./num_assets], args=args, 
                          method='SLSQP', bounds=bounds, constraints=constraints)
    

    return results


stockList = ['CBA', 'BHP', 'TLS']
stocks = [stock+'.AX' for stock in stockList] # On the Austrualian Stock Exchange

endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=365)
weights = np.array([0.3, 0.3, 0.4])

#print(getData(stocks=stocks, start_date=startDate, end_date=endDate))
meanReturns, covMatrix = getData(stocks=stocks, start_date=startDate, end_date=endDate)
returns, std = portfolioPerformance(weights=weights, meanReturns=meanReturns, covMatrix=covMatrix)
result = maxSH(meanReturns, covMatrix)
max_sr, max_weights = result['fun'], result['x']

print(f'Portfoliot Returns: {round(returns*100, 2)}\nSTD of Porfolio: {round(std, 2)}')
print(f'Max Sharpe Ratio of Portfolio: {max_sr}\nAllocation of Assets to maximize Share Ratio: {max_weights}')




