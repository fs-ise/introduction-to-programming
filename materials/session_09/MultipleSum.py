msum = 0
n = int(input("Enter the upper bound: "))
for i in range(1,n):
    if(i%3==0 or i%5==0):
        msum = msum + i
print(msum)
