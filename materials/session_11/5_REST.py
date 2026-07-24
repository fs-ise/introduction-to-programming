
import pandas as pd
stockdata = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo&datatype=csv')
stockdata.head()



import requests
r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo')
data = r.json()
data

price = data['Global Quote']['05. price']
price

price = float(data['Global Quote']['05. price'])
price

data = data['Global Quote']
price = float(data['05. price'])
price



import requests
r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo')
data = r.json()
data
dfdata = pd.DataFrame(data['Time Series (Daily)'].values(), index=data['Time Series (Daily)'].keys())

for col in list(dfdata):
    dfdata[col] = pd.to_numeric(dfdata[col])
    
dfdata = dfdata[::-1]

dfdata.plot(y='4. close', use_index=True)



import requests
import pandas as pd
r = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=eur&days=30')
data = r.json()
df = pd.DataFrame(data['prices'], columns=['time','price'])
df.head(2)

from datetime import datetime
df['time'] = pd.to_datetime(df['time'], unit='ms').dt.date
df
df.plot(x='time', y='price', rot=75)


import requests
r = requests.get('https://api.open-meteo.com/v1/forecast?latitude=50.12&'
	'longitude=8.68&daily=temperature_2m_max,temperature_2m_min&'
	'timezone=Europe%2FBerlin')
data = r.json()
data































