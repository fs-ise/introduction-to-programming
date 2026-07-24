def multi(x):
    n = len(x)
    prodX = 1.0
    for i in range(n):
        prodX = prodX * x[i]
    return prodX

li = [8, 2, 3, -1, 7, 5, 6 ]
print ("Product =", multi(li))

