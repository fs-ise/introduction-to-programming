import pandas as pd

students = pd.read_csv("Student_performance.csv")
students.head()

x = students.loc[:, ['Hours_Studied', 'Sleep_Hours', 'Exercises_Practiced']].values
y = students.loc[:, 'Performance'].values

from sklearn.linear_model import LinearRegression
predictivemodel_reg = LinearRegression()
predictivemodel_reg.fit(x, y)
y_pred = predictivemodel_reg.predict(x)
from sklearn.metrics import r2_score
r2_score(y, y_pred)
predictivemodel_reg.predict([[5, 5, 1]])

from sklearn.ensemble import RandomForestRegressor
predictivemodel_rf = RandomForestRegressor(random_state=0)
predictivemodel_rf.fit(x, y)
y_pred = predictivemodel_rf.predict(x)
from sklearn.metrics import r2_score
r2_score(y, y_pred)
predictivemodel_rf.predict([[5, 5, 1]])

from sklearn.neural_network import MLPRegressor
predictivemodel_net = MLPRegressor(solver='lbfgs', max_iter=3000, random_state=0)
predictivemodel_net.fit(x, y)
y_pred = predictivemodel_net.predict(x)
from sklearn.metrics import r2_score
r2_score(y, y_pred)
predictivemodel_net.predict([[5, 5, 1]])

