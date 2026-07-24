# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 16:32:37 2021

@author: rossbach
"""

import os
import pandas as pd

os.chdir('D:\Dropbox\Lehre\Introduction to Programming\Exercises_Python')
insurance = pd.read_excel('insurance.xlsx')
print(insurance.shape)
insurance.head()
list(insurance)
insurance.to_csv('insurance.csv', index=False)
