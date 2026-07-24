3*5
16-5
16/4
16/5
16%5
16//5
3**2
"Hello " + "World"



x = 4
x
x = 3.12
x
x = 'hello'
x

a, b = 1, 2
a
b
a + b



print('hello')
print('hello', 'there')
print('hello' + ' ' + 'there')
print('haha' * 4)
print(5 * 4)
a = 54
print(a)
print('The number is ' + str(a) + '!')
print('The number is', a, '!')

print('hello ')
print('Peter')
print('hello', end = ' ')
print('Peter')



x = 15
x = x + 5 
print(x)

x = 4
y = x + 1
x = 2
print(x, y)

a = 4.5
b = 2
print(a//b)

x = 17 / 2 % 2 * 3**3 
print(x) 

x, y = 2, 6
x, y = y, x + 2
print (x, y)

a, b = 2, 3
c, b = a, c + 1
print (a, b, c)


#-----------------------------------------------------------------------------

import pandas as pd

data = pd.read_excel('Bikesales.xlsx')
data

data.shape
list(data)
data.dtypes

import os
os.chdir(r'D:\Dropbox\Lehre\Introduction to Programming\Presentation')
data =  pd.read_csv('Bikesales.csv')


os.chdir(r'D:\Dropbox\Lehre\Introduction to Programming\Presentation')
exped = pd.read_excel('Exped.xlsx')
exped.head()

exped.to_csv('Exped.csv', index=False)

exped1 = exped
exped1 = exped1.set_index('Transid')
exped1.head()

exped['WHERE']
exped.WHERE

data.loc[1:3, :]
data.loc[1:3] 
data.loc[1:3, 'Turnover'] 
data.loc [1:3, ['Bike','Turnover']] 
data.loc [1:3, 'Bike':'Turnover'] 
data.loc [[1, 3, 6], 'Bike':'Turnover'] 
data.loc[data.Turnover>23000, :]

exped.loc[0]
exped.loc[0:2]
exped.loc[1, ['WHERE','WHAT','HOW']]
exped.loc[1:3, ['WHEN','WHERE']]

data.iloc[0,1] 
data.iloc[:,0] 
data.iloc[1:3,1] 
data.iloc[:,-2] 
data.iloc[-1,:] 
data.iloc[[0, 2], [1, 2]] 
data.iloc[[0, 2], 1:3]

exped.iloc[0]
exped.iloc[0:2]

data.loc[1:3, 'Bike':'Turnover']
data.iloc[1:3, [0,2]]
exped.loc[1:3,'WHEN':'WHERE']
exped.iloc[1:3,1:2]

data.loc['bike5'] = ['Gravelbike', 4, 14000, 9000]
data = data.drop('bike5')
data.loc[len(data)] = ['Gravelbike', 4, 14000, 9000]
data = data.drop(5)
data.loc[:, 'Profit'] = [3387, 6495, 999, 10796, 14310]
data = data.drop('Profit', axis=1)
data['Profit'] = data.Turnover - data.Cost
data['Gross_turnover'] = data.Turnover * 1.19
data = data.drop('Profit', axis=1)
data = data.drop('Gross_turnover', axis=1)

data_sorted = data.sort_values(by='Turnover')
data_sorted
data_sorted = data.sort_values(by=['Sales', 'Turnover'], ascending=False)
data_sorted

len(exped)

data['Cost'].pct_change()   # not saved

data.sum()
exped.loc[:, ['QUANTITY', 'REVENUE']].sum()
exped.iloc[:,5:7].sum()

exped.loc[:, ['QUANTITY','REVENUE']].mean()
exped['REVENUE'].std()
exped.loc[:, ['QUANTITY','REVENUE']].corr()

exped.describe()
exped['REVENUE'].describe()
exped['WHERE'].describe()

exped['WHERE'].unique()
exped['WHERE'].value_counts()

import os
import pandas as pd
os.chdir(r'D:\Dropbox\Lehre\Introduction to Programming\Presentation')
temps = pd.read_csv('temperatures.csv')
temps.head()
temps.plot()

temps.iloc[:,1:4].plot()
temps.plot(x='Month', y=['Maximum', 'Average', 'Minimum'])
temps.plot(x='Month', y=['Maximum', 'Average', 'Minimum'], xticks=range(len(temps['Month'])), rot=75)

df = exped['WHERE'].value_counts()
print(df)
df.dtypes
df.plot(kind='bar')
df.plot(kind='pie', y='WHERE')
df.plot(kind='pie', subplots=True)
df.plot(kind='pie', subplots=True, legend=True)

exped.WHERE == 'London'
exped.loc[exped.WHERE == 'London']
exped.loc[(exped.WHERE == 'London') & (exped.REVENUE >= 2500)]
exped.loc[(exped.QUANTITY >= 5) | (exped.REVENUE >= 2500)]

exped.groupby('HOW')['HOW'].count()
exped.groupby('HOW')['REVENUE'].mean()
a = exped.groupby(['HOW','WHERE'])['REVENUE'].mean()
a

