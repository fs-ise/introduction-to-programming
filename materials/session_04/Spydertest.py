##########################
# Testprogram for Spyder #
##########################

print("This is a program to test the functionality of Spyder for the module 'Introduction to Programming'.")
print("Please click with the mouse after the colon (:) in this line, then type your first name and press enter: ")
name = input()
print("you have entered:", name)

print("If you see the name typed in press Enter to continue")
input()


import pandas as pd

data = {'Number': [1, 10, 10, 7],
        'Name': ['Manuel Neuer', 'Toni Kroos', 'Lionel Messi', 'Cristiano Ronaldo'], 
        'Position': ['Goalkeeper', 'Midfielder', 'Forward', 'Striker'],
        'Goals': [0, 14, 30, 26]}
df = pd.DataFrame(data)
print(df)
print("Above, you should see a table with some data about the football players. Press Enter to continue")
input()


stockdata = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo&datatype=csv')
print(stockdata.head())
print("Above, you should see a table with some stock data. Press Enter to continue")
input()


import requests
r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo')
data = r.json()
print(data)
print("Above, you should see a some more stock data enclosed in curly brackets. Press Enter to continue")
input()


stockdata.plot(y='close', use_index=True)
print("If you click on the plots tab at the bottom of the upper right window, you should see a line chart.")







