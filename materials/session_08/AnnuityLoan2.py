amount = float(input("Enter the amount: "))
interestrate = float(input("Enter the interest rate (in %): "))
interestrate = interestrate/100.0
duration = int(input("Enter the duration (in years): "))
rating = input("Enter the rating (a, b or c): ")

if(rating == "b"):
    interestrate = interestrate * 1.1
elif(rating == "c"):
    interestrate = interestrate * 1.2

annualpayment  = amount * (((1 + interestrate) ** duration * interestrate) / ((1 + interestrate) ** duration - 1))

print("The annual payment is ", annualpayment)
