



type = input("Specify the temperature type, you enter (f or c): ")
temp = int(input("Input the  temperature you like to convert : "))

if type == "f":
  result = (9 * temp) / 5 + 32
  print("The temperature is", result, "degrees.")
elif type == "c":
  result = (temp - 32) * 5 / 9
  print("The temperature is", result, "degrees.")
else:
  print("Input proper type.")
