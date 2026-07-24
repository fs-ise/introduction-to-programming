import pandas as pd
import requests

r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=YOURKEY')
data = r.json()
#data
ibm = data["Global Quote"]["05. price"]
date_ = data["Global Quote"]["07. latest trading day"]

r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=DBK.DE&apikey=YOURKEY')
data = r.json()
#data
dt_bank = data["Global Quote"]["05. price"]

r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=XIACF&apikey=YOURKEY')
data = r.json()
#data
xiaomi = data["Global Quote"]["05. price"]

r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=NLLSF&apikey=YOURKEY')
data = r.json()
#data
nel_asa = data["Global Quote"]["05. price"]

stocks = pd.read_csv("Stocks.csv")
stocks.loc[len(stocks)] = [date_, ibm, dt_bank, xiaomi, nel_asa]
stocks.to_csv("Stocks.csv", index=False)
