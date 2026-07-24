# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 17:31:19 2020

@author: rossbach
"""

s1 = input("Enter the first string: ")
s2 = input("Enter the second string: ")
s = s1 + " " + s2

print(s)
print(len(s))
print(s[1])
print(s[4])
print(s[6])
print(s[-4:])

# if length of the string is odd
mid = len(s)//2 + 1
print(s[mid-2:mid+1])

# if length of the string is even
mid = len(s)//2
print(s[mid-2:mid+2])

print("E" in s)
print("el" in s)
