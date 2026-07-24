import pandas as pd

countries = pd.read_csv('countries.csv')

countries.groupby('Continent')['Continent'].count()
countries.groupby('Continent')['GDP'].mean()

countries['GDP_by_Pop'] = countries['GDP']/countries['Population']
countries.groupby('Continent')['GDP_by_Pop'].mean()


