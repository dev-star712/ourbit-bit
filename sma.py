import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
import yfinance as yf 
yf.pdr_override() 
sns.set()
import warnings
warnings.filterwarnings('ignore')
from itertools import product



stock =['^GSPC']
start = pd.to_datetime('2010-01-01') 
end = pd.to_datetime('2018-06-29')
data = pdr.get_data_yahoo(stock, start=start, end=end)
data['Log Returns'] = np.log(data['Adj Close']/data['Adj Close'].shift(1))
data.dropna(inplace=True)
data.head(5)
# data.to_csv('data.cvs') If we want to save the data



plt.figure(figsize = (15,9))
data['Adj Close'].plot(c = 'g')
plt.ylabel('Adjusted Close Price')
plt.show()



fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15,10))

ax1.plot(data['Log Returns'].cumsum(), c = 'r')
ax1.set_ylabel('Cumulative Log Returns')

ax2.plot(100*(np.exp(data['Log Returns'].cumsum())-1))
ax2.set_ylabel('Total Relative Returns %')

plt.show()