# Create an empty list named x.
x = []

# Ask the user to enter four integers and add them to the list.
n = int(input("Enter the first number: "))
x.append(n)
n = int(input("Enter the second number: "))
x.append(n)
n = int(input("Enter the third number: "))
x.append(n)
n = int(input("Enter the fourth number: "))
x.append(n)
print(x)

# Calculate the sum of the four numbers and insert it at the beginning of the list.
x.insert(0, x[0] + x[1] + x[2] + x[3])
print(x)

# Reverse the order of the list.
x.reverse()
print(x)

# Delete the center element of the list.
x.pop(2)

# Print the minimum and maximum values of the list.
print(min(x))
print(max(x))

# Print the last two elements of the list.
print(x[-2:])