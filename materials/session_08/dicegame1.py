
import random

stake = int(input('How much money would you like to invest? '))

dice1 = random.randint(1,6)
dice2 = random.randint(1,6)

if dice1 == dice2:
    print("You have won!!! It's a double", dice1)
    payout = stake * dice1
    print("You get", payout, "Euro!")
else:
    print("Unfortunately they lost!!! The throw brought", dice1, "and", dice2)

