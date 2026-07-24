# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

sl = []
item=input("Insert list item: ")
while item != "":
    sl.append(item)
    item=input("Insert list item: ")
for i in sl:
    print(i)

    


sl = []
item="x"
while item != "":
    item=input("Insert list item: ")
    if item!="":
        sl.append(item)
for i in sl:
    print(i)




sl = []
item="x"
while item != "":
    item=input("Insert list item: ")
    if item=="":
        break
    sl.append(item)
for i in sl:
    print(i)
