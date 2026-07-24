
x = float(input("Enter the taxable income: "))
 
if x < 11604:
    t = 0
    
if 11604 < x <= 17005:
    y = (x - 11604) / 10000
    t = (922.98 * y + 1400) * y
    
if 17005 < x <= 66760:
    z = (x - 17005) / 10000
    t = (181.19 * z + 2397) * z + 1025.38
     
if 66760 < x <= 277825:
    t = 0.42 * x - 10602.13
    
if 277825 < x:
    t = 0.45 * x - 18936.88
        
ni = x - t
    
print("The tax to pay is ", t)
print("The net income is ", ni)
