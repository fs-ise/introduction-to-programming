import pandas as pd

countries = pd.read_csv('data/countries.csv')
print(countries.shape)
countries.head()
print(countries.columns) # or print(list(countries))
