
import requests
import pandas as pd

r = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=eur&days=30')
data = r.json()
btc = pd.DataFrame(data['prices'], columns=['time','price'])
btc.head(3) 

r = requests.get('https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=eur&days=30')
data = r.json()
eth = pd.DataFrame(data['prices'], columns=['time','price'])
eth.head(3) 

compare = pd.DataFrame(btc.time)
compare['BTC'] = btc.price
compare['ETH'] = eth.price

compare['BTC_returns'] = compare['BTC'].pct_change()
compare['ETH_returns'] = compare['ETH'].pct_change()

compare['time'] = compare['time'].astype('object')
from datetime import datetime
for i in range(len(compare)):
    compare.iloc[i, 0] = datetime.fromtimestamp(int(compare.iloc[i, 0])/1000).date()

compare['BTC_returns'].var()
compare['ETH_returns'].var()

compare.loc[:,['BTC_returns', 'ETH_returns']].corr()
compare['BTC_returns'].corr(compare['ETH_returns'])

compare.plot(x='time', y=['BTC_returns', 'ETH_returns'], rot=75)
