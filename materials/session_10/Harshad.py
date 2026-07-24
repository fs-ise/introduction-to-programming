def isHarshad(num):
    num_string = str(num)
    num_sum = 0
    for i in range(len(num_string)):
        num_sum = num_sum + int(num_string[i])
    if (num%num_sum==0):
        return True
    else:
        return False

number = int(input("Please enter a number: "))
print(isHarshad(number))