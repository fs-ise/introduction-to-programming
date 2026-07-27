import pandas as pd

countries = pd.read_csv('../materials/data/countries.csv')
print(countries.shape)
print(countries.columns) # or print(list(countries))
countries.head()

