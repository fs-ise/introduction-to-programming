
import pandas as pd

stockdata = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MBG.DEX&outputsize=full&apikey=YOURKEY&datatype=csv')
stockdata = stockdata[::-1]
stockdata.plot(x='timestamp', y='close', rot=75)
stockdata.loc[:, 'return'] = stockdata.loc[:, 'close'].pct_change()
stockdata.plot(x='timestamp', y='return', rot=75)
