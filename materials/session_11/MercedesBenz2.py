
import pandas as pd
import requests

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MBG.DEX&outputsize=full&YOURKEY'
r = requests.get(url)
data = r.json()
stockdata = pd.DataFrame(data['Time Series (Daily)'].values(), index=data['Time Series (Daily)'].keys())
for col in list(stockdata):
	stockdata[col] = pd.to_numeric(stockdata[col])
stockdata = stockdata[::-1]
stockdata.plot(y='4. close', use_index=True, rot=75)
stockdata.loc[:, '6. return'] = stockdata.loc[:, '4. close'].pct_change()
stockdata.plot(y='6. return', use_index=True, rot=75)
