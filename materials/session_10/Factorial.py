# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 11:15:52 2017

@author: PeterRossbach
"""

def factorial(n):
    fac = 1
    for i in range(1, n+1):
        fac = fac * i
    return fac

n = int(input("Enter a number: "))
print ("Factorial =", factorial(n))

