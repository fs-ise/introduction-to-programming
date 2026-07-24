# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 19:42:12 2017

@author: rossb
"""

amount = float(input("Enter the amount: "))
interestrate = float(input("Enter the interest rate (in %): "))
interestrate = interestrate/100.0
duration = int(input("Enter the duration (in years): "))
   
annualpayment  = amount * (((1 + interestrate) ** duration * interestrate) / 
                           ((1 + interestrate) ** duration - 1))
   
print("The annual payment is ", round(annualpayment,2))
