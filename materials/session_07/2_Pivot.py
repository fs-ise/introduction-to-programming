import os
import pandas as pd

os.chdir('D:\Dropbox\Lehre\Introduction to Programming\Presentation')
sales = pd.read_excel('Sales.xlsx')
print(sales.shape)
sales.head()
list(sales)

pd.pivot_table(sales, index = 'Region', values = 'Turnover', aggfunc = 'sum')
pd.pivot_table(sales, index = 'Region', columns = 'Product', values = 'Turnover', aggfunc = 'sum')


pd.pivot_table(sales.loc[sales.Category=='Actual'], index = 'Region', values = 'Turnover', aggfunc = 'sum')
pd.pivot_table(sales[sales.Category=='Actual'], index = 'Region', values = 'Turnover', aggfunc = 'sum')
pd.pivot_table(sales[sales.Category=='Actual'], index = 'Region', values = 'Turnover', aggfunc = ['sum', 'mean', 'std'])
pd.pivot_table(sales[sales.Category=='Actual'], index = 'Region', values = 'Turnover', columns = 'Product', aggfunc = 'sum')
pd.pivot_table(sales[(sales.Category=='Actual') & (sales.Year==2020)], index = 'Region', values = 'Turnover', columns = 'Product', aggfunc = 'sum')

pivot_df = pd.pivot_table(sales[(sales.Category=='Actual') & (sales.Year==2020)], index = 'Region', values = 'Turnover', columns = 'Product', aggfunc = 'sum')
pivot_df.sum()
pivot_df.loc['Total'] = pivot_df.sum()
print(pivot_df)
pivot_df.plot(kind='bar')

pd.pivot_table(sales[sales.Category=='Actual'], index = ['Year', 'Region'], values = 'Turnover', columns = 'Product', aggfunc = 'sum')

