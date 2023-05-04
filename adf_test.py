#!/usr/bin/bash python3

from statsmodels.tsa.stattools import adfuller

def adf_test(timeseries, display=True):
    #print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    if display:
        print (dfoutput)
    return float(dfoutput['p-value'])
# Call the function and run the test

#adf_test(lat_int[:20])

fig, ax = plt.subplots()
ax.plot([adf_test(lat_int[:i], False) for i in range(5,150)])
ax.axhline(0.05)
plt.show()


