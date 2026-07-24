
n = int(input("How many numbers should be generated: "))
fib = [0,1]
for i in range(n):
    fib.append(fib[-2]+fib[-1])
print(fib)


