def multiply(list_of_numbers):
    product = 1
    for value in list_of_numbers:
        product = product * value
    return product


li = [8, 2, 3, -1, 7, 5, 6]
print("Product =", multiply(li))
