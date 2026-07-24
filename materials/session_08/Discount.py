
amount = float(input("Input the purchase amount: "))

if amount >= 100:
    discount = 20
elif amount >= 50:
    discount = 10
else:
    discount = 0

print("Discount: " + str(discount) + "%");