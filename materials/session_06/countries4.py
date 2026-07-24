import pandas as pd

countries = pd.read_csv('countries.csv')

countries.plot(x='Country', y=['Population', 'Area', 'GDP'],
               xticks=range(len(countries['Country'])), rot=75)

df = countries['Continent'].value_counts()
df.plot(kind='bar')
df.plot(kind='pie')

countries.plot(kind='density', y='GDP')
countries.plot(kind='box', y='GDP')



