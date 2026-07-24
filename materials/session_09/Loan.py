amount = float(input("Amount of the loan: "))
repayment = float(input("Repayment: "))
irate = float(input("Interest rate (in % and annual): "))

period = 0
while amount>0.0:
    period += 1
    interest = amount * irate/100.0/12.0
    if (amount>repayment):
        amount = amount - repayment
    else:
        repayment = amount
        amount = amount - repayment
    print ("Month:", period, " Repayment:", repayment, " interest:", round(interest,2), " Remaining:", amount)