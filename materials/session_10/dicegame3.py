
import random

stake = int(input('How much money would you like to invest? '))
continue_ = True

while continue_:
    pasch = False
    try_ = 1
    while pasch==False and try_<4:
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        print("The throw brought", dice1, "and", dice2)
        if dice1==dice2:
            pasch = True
            break
        try_ = try_ + 1

    if pasch==True:
        print("You have won!!! It's a double", dice1)
        payout = stake * dice1
        print("You get", payout, "Euro!")
        continue_ = bool(int(input('Would you like to continue? 1=yes, 0=no: ')))
        if continue_:
            stake = payout
    else:
        print("Unfortunately you have lost!!!")
        continue_ = False


