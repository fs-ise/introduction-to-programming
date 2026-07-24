import pandas as pd

countries = pd.read_csv('countries.csv')

countries['Area'].sum()
countries['GDP'].mean()
countries['GDP'].var()

countries.loc[:, ['Population', 'Area', 'GDP']].mean()
countries.loc[[2, 10, 11, 13], ['Population', 'Area', 'GDP']].mean()

countries['Area'].min()

countries.loc[:, ['Population', 'Area', 'GDP']].corr()

countries.describe()    # or: countries[['Population', 'Area', 'GDP']].describe()

countries.loc[:, ['Country', 'Continent']].describe()

len(countries['Continent'].unique())
countries['Continent'].value_counts()


