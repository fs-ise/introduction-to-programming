import os
import pandas as pd

os.chdir('D:\Dropbox\Lehre\Introduction to Programming\Exercises_Python')
countries = pd.read_csv('countries.csv')

countries.groupby('Continent')['Continent'].count()
countries.groupby('Continent')['GDP'].mean()

countries['GDP_by_Pop'] = countries['GDP']/countries['Population'] 
countries.groupby('Continent')['GDP_by_Pop'].mean()


