
import random

n = int(input("How many random numbers do you want to generate? "))
freqlist = [0,0,0,0,0,0,0,0,0,0]
for i in range(n):
    x = random.randint(1,10)
    freqlist[x-1] = freqlist[x-1] + 1
print(freqlist)