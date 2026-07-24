s = input ("Input a String: ")
half = len(s)//2
s1 = input("String to insert: ")
s_new = s[:half] + s1 + s[half:]
print ('The new string is ' + s_new)
