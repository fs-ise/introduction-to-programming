# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 19:42:12 2017

@author: rossb
"""

kilometers = float(input("Enter your driven kilometers: "))
volume = float(input("Enter the quantity of petrol tanked : "))

consumption = volume*100/kilometers

print("Your car consumes", consumption, " liters per 100 km.")
