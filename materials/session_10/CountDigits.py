def count_digitsa(number):
    snum = str(number)
    count = len(snum)
    return count

def count_digitsb(number):
    count = 0
    while number>0:
        number = number//10
        count = count + 1
    return count

number = int(input("Please enter a number: "))
print("The number of Digits is", count_digitsa(number))
print("The number of Digits is", count_digitsb(number))