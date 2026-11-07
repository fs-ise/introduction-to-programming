# a) Store the values 'Audi', 'VW', 'BMW', 'Honda', and 'Mercedes' in a list.
cars = ['Audi', 'VW', 'BMW', 'Honda', 'Mercedes']

# b) Print 'BMW' and 'Honda' using their positions in the list.
print(cars[2:4])

# c) Print a statement about your favorite car manufacturer using its position.
# For example: 'A great car manufacturer is value.'
print('A great car manufacturer is ' + cars[0] + '.')

# d) Expand the list by adding a car manufacturer of your choice.
cars.append('Volvo')

# e) Retrieve the number of car manufacturers in your list.
len(cars)

# f) Retrieve the position of 'Honda' in the list.
cars.index('Honda')

# g) Delete 'Honda' from the list.
cars.remove('Honda')

# h) Print the content of the last position in the list.
print(cars[-1])