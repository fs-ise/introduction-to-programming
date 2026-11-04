import pandas as pd

# 1 Read the file "Homes_Florida.xlsx" into a dataframe named homes.
homes = pd.read_excel("data/Homes_Florida.xlsx")

# 2 Create a new column named Profit that contains
# the profit made on each house transaction.
homes["Profit"] = homes.Sales_Price - homes.Purchase_Price

# 3 What profit did the agency "Orlando" make?
homes.loc[homes.Agency == "Orlando", "Profit"].sum()

# 4 Determine the profits made in each area, then visualize them in a bar chart.
homes.groupby("Area")["Profit"].sum()
homes.groupby("Area")["Profit"].sum().plot(kind="bar", x="Area", y="Profit")

# 5 Calculate the average profit as a percentage of the sales price
# for houses smaller than 2,000.
(
    homes.loc[homes.Size < 2000, "Profit"]
    / homes.loc[homes.Size < 2000, "Sales_Price"]
).mean() * 100

# 6 How many houses that are 6 years old are larger than 2,000 square meters?
homes.loc[(homes.Age == 6) & (homes.Size > 2000)].count()
homes.loc[(homes.Age == 6) & (homes.Size > 2000), "ID"].count()

# 7 How many houses with 3 or 4 bedrooms are older than 6 years?
homes.loc[
    (homes.Bedrooms >= 3) & (homes.Bedrooms <= 4) & (homes.Age > 6), "ID"
].count()
homes.loc[
    ((homes.Bedrooms == 3) | (homes.Bedrooms == 4)) & (homes.Age > 6), "ID"
].count()

# 8 Create a frequency distribution of profits.
homes["Profit"].plot(kind="hist")

# 9 How many unique agency names does the company have? This returns their count.
homes["Agency"].nunique()

# 10 Show the mean sales value and its standard deviation for each agency.
pd.pivot_table(homes, index="Agency", values="Sales_Price", aggfunc=["mean", "std"])

# 11 Show the correlations between the purchase price
# and the variables Size, Bedrooms, and Age.
homes.loc[:, ["Age", "Bedrooms", "Size", "Purchase_Price"]].corr().loc[
    ["Age", "Bedrooms", "Size"], "Purchase_Price"
]

# 12 In which area is the most expensive house, and how many bedrooms does it have?
homes.loc[homes.Purchase_Price == homes.Purchase_Price.max(), ["Area", "Bedrooms"]]

# 13 Create a forecast model for the house price based on a Linear Regression.
x = homes.loc[:, ["Age", "Size", "Bedrooms"]]
y = homes.Purchase_Price

from sklearn.linear_model import LinearRegression

forecastmodel = LinearRegression()
forecastmodel.fit(x, y)

forecasts = forecastmodel.predict(x)
from sklearn.metrics import r2_score

r2_score(y, forecasts)

forecastmodel.predict([[5, 2000, 3]])

# 14 Create a forecast model based on a Decision Tree.
from sklearn.tree import DecisionTreeRegressor

# forecastmodel = DecisionTreeRegressor(random_state=0)
forecastmodel = DecisionTreeRegressor(max_depth=3, random_state=0)
forecastmodel.fit(x, y)

from sklearn.tree import plot_tree

plot_tree(forecastmodel, feature_names=list(x), filled=True)

forecasts = forecastmodel.predict(x)
from sklearn.metrics import r2_score

r2_score(y, forecasts)

forecastmodel.predict([[5, 2000, 3]])

# 15 Create a forecast model based on a Neural Network.
from sklearn.neural_network import MLPRegressor

forecastmodel = MLPRegressor(solver="lbfgs", random_state=0)
forecastmodel.fit(x, y)

forecasts = forecastmodel.predict(x)
from sklearn.metrics import r2_score

r2_score(y, forecasts)

forecastmodel.predict([[5, 2000, 3]])
