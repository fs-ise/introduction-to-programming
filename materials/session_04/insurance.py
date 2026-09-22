import pandas as pd

insurance = pd.read_excel('data/insurance.xlsx')
print(insurance.shape)
print(insurance.head())
print(list(insurance))
# insurance.to_csv('outputs/insurance.csv', index=False)
