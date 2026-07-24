score = int(input("Input a score (in %): "))
if score<50:
  grade = "F"
elif score<59:
  grade = "E"
elif score<69.5:
  grade = "D"
elif score<80:
  grade = "C"
elif score<90.5:
  grade = "B"
else:
  grade = "A"
print("The grade is: ", grade)
