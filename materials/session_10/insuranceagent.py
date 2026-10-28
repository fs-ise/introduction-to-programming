commission = 0

while True:
    sum_insured = float(input("Sum insured: "))
    if sum_insured != 0:
        commission = commission + 50 + sum_insured * 0.01
    else:
        break

print("Commission:", commission)
