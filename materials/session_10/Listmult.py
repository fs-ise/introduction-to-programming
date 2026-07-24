# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 11:15:52 2017

@author: PeterRossbach
"""

def multi(x):
    n = len(x)
    prodX = 1.0
    for i in range(n):
        prodX = prodX * x[i]
    return prodX

li = [8, 2, 3, -1, 7, 5, 6 ]
print ("Product =", multi(li))

