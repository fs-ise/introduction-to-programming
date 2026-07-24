import pandas as pd

insurance = pd.read_excel('insurance.xlsx')
print(insurance.shape)
insurance.head()
list(insurance)
insurance.to_csv('insurance.csv', index=False)
