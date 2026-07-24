# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 16:32:37 2021

@author: rossbach
"""

import os
import pandas as pd

os.chdir('D:\Dropbox\Lehre\Introduction to Programming\Exercises_Python')
insurance = pd.read_excel('insurance.xlsx')

insurance.groupby('State')['InsuredValue'].mean()
pd.options.display.float_format = '{:.2f}'.format
insurance.groupby('State')['InsuredValue'].mean()
insurance.groupby('State')['InsuredValue'].count()
insurance.loc[insurance['Flood'] == 'Y'].groupby('State')['InsuredValue'].count()
insurance.loc[(insurance['Flood'] == 'Y') | (insurance['Earthquake'] == 'Y')].groupby('State')['InsuredValue'].count()

