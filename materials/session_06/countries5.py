import os
import pandas as pd

os.chdir('D:\Dropbox\Lehre\Introduction to Programming\Exercises_Python')
countries = pd.read_csv('countries.csv')

countries.loc[countries.Area > 8000]

countries.loc[countries.Area > 8000, 'GDP'].mean()
countries.loc[countries.Area < 800, 'GDP'].mean()

countries.loc[(countries.Area > 8000) & (countries.Population < 400)]
countries.loc[(countries.Area > 8000) & (countries.Population < 400), ['Country', 'GDP']]

df = countries.loc[(countries.Area > 8000) & (countries.Population < 400), ['Country', 'GDP']]
df.plot(x='Country', kind='bar', rot=0)

df = countries.loc[countries.Population < 100, 'Continent'].value_counts()
df.plot(kind='pie', y='Continent')

df = countries.loc[countries.Continent == 'Europe', 'GDP']
df.plot(kind='density')




