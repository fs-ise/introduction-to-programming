import pandas as pd

houses = pd.read_excel('Homes_Florida.xlsx')

#1 Erzeugen Sie eine neue Spalte namens Profit, die den bei den Haustransaktionen erzielten Gewinn enthält.
houses['Profit'] = houses.Sales_Price - houses.Purchase_Price

#2 Welchen Gewinn hat die Agency "Orlando" erzielt?
houses.loc[houses.Agency=='Orlando', 'Profit'].sum()

#3 Ermitteln Sie die Gewinne, die pro Area gemacht wurden. Visualisieren Sie diese anschließend in einem Bar-Chart.
houses.groupby('Area')['Profit'].sum()
houses.groupby('Area')['Profit'].sum().plot(kind='bar', x='Area', y='Profit')

#4 Ermitteln Sie die durchschnittlichen Gewinne in Prozent von Häusern, deren Size kleiner als 2000 ist.
(houses.loc[houses.Size<2000, 'Profit']/houses.loc[houses.Size<2000, 'Sales_Price']).mean()*100

#5 Wie viele Häuser mit einem Alter von 6 Jahren sind größer als 2000 qm?
houses.loc[(houses.Age==6) & (houses.Size>2000)].count()
houses.loc[(houses.Age==6) & (houses.Size>2000), 'ID'].count()

#6 Wie viele Häuser mit 3 oder 4 Bedrooms sind älter als 6 Jahre?
houses.loc[(houses.Bedrooms>=3) & (houses.Bedrooms<=4) & (houses.Age>=6), 'ID'].count()
houses.loc[((houses.Bedrooms==3) | (houses.Bedrooms==4)) & (houses.Age>=6), 'ID'].count()

#7 Erstellen Sie eine Häufigkeitsverteilung der Profite.
houses['Profit'].plot(kind='hist')

#8 Wie viele Agencies hat das Unternehmen?
houses['Agency'].unique()

#9 Zeigen Sie den mittleren Verkaufswert und dessen Standardabweichung pro Agency an.
pd.pivot_table(houses, index='Agency', values='Purchase_Price', aggfunc=['mean', 'std'])

#10 Stellen Sie die statistischen Zusammenhänge (Korrelationen) zwischen dem Purchase_Preis und den Variablen Size, Bedrooms und Age dar.
houses.loc[:, ['Age', 'Bedrooms', 'Size', 'Purchase_Price']].corr().loc[['Age', 'Bedrooms', 'Size'], 'Purchase_Price']

#11 In welcher Area steht das teuerste Haus und wie viele Zimmer hat es?
houses.loc[houses.Purchase_Price==houses.Purchase_Price.max(), ['Area', 'Bedrooms']]

#12 Create a forecast model for the house price based on a Linear Regression
x = houses.loc[:, ['Age', 'Size', 'Bedrooms']]
y = houses.Purchase_Price

from sklearn.linear_model import LinearRegression
forecastmodel = LinearRegression()
forecastmodel.fit(x, y)

forecasts = forecastmodel.predict(x)
from sklearn.metrics import r2_score
r2_score(y, forecasts)

forecastmodel.predict([[5, 2000, 3]])

#13 Create a forecast model based on a decision tree
from sklearn.tree import DecisionTreeRegressor
#forecastmodel = DecisionTreeRegressor(random_state=0)
forecastmodel = DecisionTreeRegressor(max_depth=3, random_state=0)
forecastmodel.fit(x, y)

from sklearn.tree import plot_tree
plot_tree(forecastmodel, feature_names=list(x), filled=True)

forecasts = forecastmodel.predict(x)
from sklearn.metrics import r2_score
r2_score(y, forecasts)

forecastmodel.predict([[5, 2000, 3]])

#14  Create a forecast model based on a Neural Network
from sklearn.neural_network import MLPRegressor
forecastmodel = MLPRegressor(solver='lbfgs', random_state=0)
forecastmodel.fit(x, y)

forecasts = forecastmodel.predict(x)
from sklearn.metrics import r2_score
r2_score(y, forecasts)

forecastmodel.predict([[5, 2000, 3]])








