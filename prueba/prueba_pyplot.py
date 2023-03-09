from matplotlib import rcParams, pyplot as plt
import pandas as pd
import pandas_datareader as pdr

import os
from datetime import datetime
import pandas_datareader.data as web
import numpy as np

# a = web.get_quote_av(['AAPL', 'TSLA'])
# print(a)


stocks = ['GOOG', 'AMZN']
data = pdr.get_data_yahoo(stocks, start= '2019-01-01')['Close']
maxY = max([max(data[x]) for x in data.columns])
minY = min([min(data[x]) for x in data.columns])
rcParams['figure.figsize'] = 15,6
plt.plot(data.GOOG, color = 'green')
plt.plot(data.AMZN, color = 'orange')
plt.legend(loc=5)
plt.grid(True, color = 'k', alpha = .25)
plt.title('Arbitrage')
plt.ylim(maxY + 100, minY-100)
plt.style.use('ggplot')
plt.yticks(np.linspace(0,maxY,5))
plt.show()
