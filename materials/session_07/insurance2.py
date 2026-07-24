import os
import pandas as pd

os.chdir('D:\Dropbox\Lehre\Introduction to Programming\Exercises_Python')
insurance = pd.read_excel('insurance.xlsx')

pd.options.display.float_format = '{:.2f}'.format
pd.pivot_table(insurance, index = 'State', values = 'InsuredValue', aggfunc = 'mean')

pd.pivot_table(insurance, index = 'State', columns = 'Location', values = 'InsuredValue',
               aggfunc = 'mean', fill_value=0)

# Remark: The parameter fill_value=0 replaces NaN with 0 !!!

pd.pivot_table(insurance[(insurance.Flood=='Y') & (insurance.Earthquake=='Y')],
               index = 'State', columns = 'Region', values = 'InsuredValue',
               aggfunc = 'mean', fill_value=0)

pd.pivot_table(insurance[(insurance.Flood=='Y') & (insurance.Earthquake=='Y')],
               index = 'State', columns = 'Construction', values = 'InsuredValue',
               aggfunc = 'mean', fill_value=0)

pd.pivot_table(insurance, index = ['Location', 'BusinessType'], columns = 'Region',
               values = 'InsuredValue', aggfunc = 'sum', fill_value=0)

pivot_df = pd.pivot_table(insurance, index = ['Location', 'BusinessType'],
                          columns = 'Region', values = 'InsuredValue', aggfunc = 'sum', fill_value=0)
pivot_df.loc['Total'] = pivot_df.sum()
print(pivot_df)

pivot_df = pd.pivot_table(insurance, index = 'Location', columns = 'State',
                          values = 'InsuredValue', aggfunc = 'count', fill_value=0)
pivot_df.plot(kind='bar')

