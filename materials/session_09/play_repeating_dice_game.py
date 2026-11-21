import random

stake = int(input("How much money would you like to invest? "))
play_another_round = True

while play_another_round:
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)

    if dice1 == dice2:
        print("You have won!!! It's a double", dice1)
        payout = stake * dice1
        print("You get", payout, "Euro!")
        play_another_round = bool(int(input("Would you like to continue? 1=yes, 0=no: ")))
        if play_another_round:
            stake = payout
    else:
        print("Unfortunately they lost!!! The throw brought", dice1, "and", dice2)
        play_another_round = False
