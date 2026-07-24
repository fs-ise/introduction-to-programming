127
x = -127
x 
type(x)

-236.4532 
12398741634341798.132 
x = 0.0000000000234234 
x 
type(x)



name = input("What's your name? ")
print("Nice to meet you " + name + "!")
age = input("Your age? ")
print("So, you are already " + age + " years old, " + name + "!")
type(age)
age = int(input("Your age? "))
type(age)



12 > 11 
x = True
x
x = bool(1) 
x
answer = ( 2*3 == 6 ) 
answer 



var1 = 'Hello World!' 
var2 = "Python Programming"
x = 'abc'
type(x)
y = '"A quotation!"'
print(y)



s = 'Don Quijote'

s[:6] + s[6:]



list1 = ['physics', 'chemistry', 1997, 2000] 
list2 = [1, 2, 3, 4, 5 ]
list3 = ["a", "b", "c", "d"] 
list4 = [[1,2,3,4], [5,6,7,8], [9,10,11,12]]




x = [0,1,2,3,4,5,6,7,8,9]



tuple1 = ('physics', 'chemistry', 1997, 2000) 
tuple2 = (1, 2, 3, 4, 5 )
tuple3 = ("a", "b", "c", "d") 
tuple4 = ((1,2,3,4), (5,6,7,8)) 

tuple1[1]
tuple2[2:4]
tuple4[1][2:4]



mylist = [1,2,3,4]
mytupel = (1,2,3,4)
print(mylist)
print(mytupel)
mylist[2] = 5
print(mylist)
mytupel[2] = 5



if x < 1:
  print("x smaller than 1") 

if x < 1: 
   print("x smaller than 1") 
else: 
   print("x is bigger than or equal to 1") 

if x < 1: 
   print("x smaller than 1") 
elif x == 1: 
   print("x is equal to 1") 
else: 
   print("x is bigger than 1") 

# swap x and y if y<x
print(x, y)
if y < x:
    temp = x
    x = y
    y = temp
print(x, y)

if time >= 11 and time <= 13:
    print("It is noon!")



list(range(10))
list(range(6,10))
list(range(1,10,2)) 

for i in range(3):
    print(i)

for i in [2,9,7]:
    x = i * 2
    print(x)

for i in ['apple', 'orange']:
    print(i)




count = 0
while (count < 4):
     print("The count is:", count)
     count = count + 1

names = ['Ann', 'Tom', 'Peter', 'Jens', 'Sue']
while names[0]!='Jens':
     print(names[0])
     names.remove(names[0]) 



for val in "string":
    if val == "i":
        break
    print(val)
print("The end")

for val in "string":
    if val == "i":
        continue
    print(val)
print("The end")





def square(x):
    sq = x*x
    return sq
# Call the function
x = 2
y = square(x)
print(x,y)

def add(x,y):
    return x+y
# Call the function
x = 2
y = 3
z = add(x,y)
print(x,y,z)

def fibonacci(n):
    fib = [0,1]
    for i in range(n):
        fib.append(fib[-2]+fib[-1])
    return fib    
# Call the function
n = int(input("How many numbers: "))
print(fibonacci(n))


def square(x):
    sq = x*x
    return sq
def sumofSquares(numberlist):
    sum_ = 0
    for i in numberlist:
        squaredValue = square(i)
        sum_ += squaredValue
    return sum_
# Main Program
a = 2
b = 3
c2 = square(a) + square(b)    # apply Pythagoras  
print(c2)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
total = sumofSquares(numbers)
print("Sum of the Square of List of Numbers:", total)




import math 
print(math.sin(5))
print(math.sin(math.pi))




dict1 = {'Peter': 55, 'Mary': 40, 'Bob': 34}
dict1

dict1['Mary']
dict1['Hans']
dict1[0]

a = 'Peter'
dict1[a]

dict1['Alice'] = 55
dict1

dict1['Mary'] = 41
dict1

stockprices =	{'Date': ['1.1.2021', '2.1.2021', '1.1.2021', '2.1.2021'],
               'BMW': [89, 91, 95, 92],
               'Telekom': [12, 10, 14, 17],
               'SAP': [114, 119, 125, 130]}

contacts = {
    'name': 'Alice',
    'age': 30,
    'address': {
        'street': '123 Main St',
        'city': 'Wonderland',
        'zip': '12345'
    },
    'phone_numbers': [
        {'type': 'home', 'number': '123-456-7890'},
        {'type': 'work', 'number': '987-654-3210'}
    ]
}

product_details = {
    'product_id': 101,
    'name': 'Laptop',
    'price': 799.99,
    'in_stock': True,
    'tags': ['electronics', 'computer']
}

item_quantities = {
    1: 50,
    2: 30,
    3: 75
}


students = {
    'student1': {
        'name': 'John',
        'age': 22,
        'courses': ['Math', 'Science']
    },
    'student2': {
        'name': 'Jane',
        'age': 24,
        'courses': ['History', 'Literature']
    }
}

students['student1']
students['student1']['age']
students['student1']['courses']
students['student1']['courses'][0]
students['student1']['haircolor'] = 'blonde'    # add a new key-value pair
students['student1']['courses'].append('Informatics')    # add a new list element
students['student1']

students['student3'] ={'name': 'Peter', 'age': 25, 'courses': ['Finance']}
students['student3']['weight'] = 23

del students['student3']['weight']
del students['student3']

students['student2']['courses'].append('Informatics') 

students['student1']['courses'].remove('Math') 

students['student1'] ={'age': 25} 


import json
file = open('students.db', 'w')
json.dump(students, file)
file = open('students.db', 'r')
students = json.load(file)




import pandas as pd
data = pd.read_csv('Stockprice.csv')
data.head()
data['MA10'] = None    # create an empty column 
n = 10
for i in range(n, len(data)):
            data.iloc[i, 2] = data.iloc[(i-n):i, 1].mean()
data.head()
data.head(15)
data.plot(y=['price', 'MA10'], use_index=True)

def semivariance(values):
    average = values.mean()
    sum = 0
    count = 0
    for i in range(len(values)):
        if i < average:
            sum = sum + (values.iloc[i]-average)**2
            count = count + 1
    semivar = sum/count
    return semivar

semivariance(data['price'])





