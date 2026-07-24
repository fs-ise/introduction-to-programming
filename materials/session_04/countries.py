import os
import pandas as pd

os.chdir('D:\Dropbox\Lehre\Introduction to Programming\Exercises_Python')
countries = pd.read_csv('countries.csv')
print(countries.shape)
list(countries)
countries.head()

