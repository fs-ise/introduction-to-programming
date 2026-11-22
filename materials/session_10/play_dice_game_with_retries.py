import random

stake = int(input("How much money would you like to invest? "))
play_again = True

while play_again:
    rolled_doubles = False
    attempt = 1
    while rolled_doubles == False and attempt < 4:
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        print("The throw brought", dice1, "and", dice2)
        if dice1 == dice2:
            rolled_doubles = True
            break
        attempt = attempt + 1

    if rolled_doubles == True:
        print("You have won!!! It's a double", dice1)
        payout = stake * dice1
        print("You get", payout, "Euro!")
        play_again = bool(int(input("Would you like to continue? 1=yes, 0=no: ")))
        if play_again:
            stake = payout
    else:
        print("Unfortunately you have lost!!!")
        play_again = False
