n = int(input("How many numbers do you want to enter: "))
numbers = []
for i in range(n):
    numbers.append(int(input("Enter number: ")))
sum = 0
for i in range(n):
    sum = sum + numbers[i]
average = sum/n
print("The average is: ", average)