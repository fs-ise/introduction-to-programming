import random
target_num = random.randint(1, 10)
guess_num = 0
while target_num != guess_num:
    guess_num = int(input('Guess a number between 1 and 10 until you get it right: '))
print('Well guessed!')

