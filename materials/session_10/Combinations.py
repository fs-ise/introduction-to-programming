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

def combinations(n,k):
    return (factorial(n)/(factorial(n-k)*factorial(k)))

n = int(input("Enter n: "))
k = int(input("Enter k: "))
print ("Combinations =", combinations(n,k))

