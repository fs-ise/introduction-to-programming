
an = input('Enter the account number: ')
bc = input('Enter the bank code: ')
cc = input('Enter the county code as a number (e.g. 1314 for DE): ')

base_string = bc + an + cc + '00'
base_number = int(base_string)

validation_number = 98 - base_number%97
print(validation_number)