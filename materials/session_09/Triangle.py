
word = input("Enter a word: ")

for i in range(len(word)):
    for j in range(i+1):
        print(word[i], end="")
    print()