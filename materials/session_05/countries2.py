import os
import pandas as pd

os.chdir('D:\Dropbox\Lehre\Introduction to Programming\Exercises_Python')
countries = pd.read_csv('countries.csv')

countries.loc[len(countries)] = ['Belgium',11.5,11.849,803.166,'Europe']

countries.sort_values(by='Country')

countries['GDP_per_capita'] = countries.GDP / countries.Population

countries.sort_values(by='GDP_per_capita', ascending=False)

countries = countries.drop('GDP_per_capita', axis=1)

countries = countries.drop(20)


