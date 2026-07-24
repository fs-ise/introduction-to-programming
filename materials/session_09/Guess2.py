import random
target_num = random.randint(1, 100)
guess_num = 0
while target_num != guess_num:
    guess_num = int(input("Guess a number: "))
    if(target_num<guess_num):
        print("lower")
    elif(target_num>guess_num):
        print("higher")
print('Well guessed!')

