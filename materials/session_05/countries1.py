import pandas as pd

countries = pd.read_csv('countries.csv')

countries['Country']
countries.Country

countries.iloc[:, [0, 3]]
countries.iloc[1:5, 0:3]
countries.iloc[[11, 6, 14], [0, 3]]

countries.loc[:, ['Country', 'GDP']]
countries.loc[2:5, ['Country', 'GDP']]
countries.loc[4:13, ['Country', 'Continent', 'Area']]

