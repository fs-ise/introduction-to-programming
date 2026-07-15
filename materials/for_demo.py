
n = 5
for i in range(n):
    print(i)


n = 5
for i in range(n):
    print(i, end="")


n = 5
for i in range(n):
    for j in range(n):
        print(i, j)


n = 5
for i in range(n):
    for j in range(n):
        print(i, j, end=" | ")
    print()


n = 5
for i in range(n):
    for j in range(i+1):
        print(i, j, end=" | ")
    print()


s = "Hallo"
n = 5
for i in range(n):
    print(s[i])


s = "Hallo"
for i in range(len(s)):
    print(s[i])


s = "Hallo"
for i in range(len(s)):
    print(s[i], end="")


s = "Hallo"
for i in range(len(s)):
    for j in range(i+1):
        print(s[i], end="")
    print()


s = "Hallo"
for i in s:
    print(i)







