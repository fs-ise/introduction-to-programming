import pandas as pd

insurance = pd.read_excel('../materials/data/insurance.xlsx')
print(insurance.shape)
print(insurance.head())
print(list(insurance))
# insurance.to_csv('insurance.csv', index=False)
