# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 17:31:19 2020

@author: rossbach
"""


x = []
n = int(input("Enter the first number: "))
x.append(n)
n = int(input("Enter the second number: "))
x.append(n)
n = int(input("Enter the third number: "))
x.append(n)
n = int(input("Enter the fourth number: "))
x.append(n)
print(x)
x.insert(0, x[0]+x[1]+x[2]+x[3])
print(x)
x.reverse()
print(x)
x.remove(2)
print(min(x))
print(max(x))
print(x[-2:])
