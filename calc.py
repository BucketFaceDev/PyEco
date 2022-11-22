numberA = input("Input a number: ")
numberB = input("Input a second number: ")
operator = input ("Input an operand: ")

availableOperators = ["+", "-", "/", "*"]

if(operator in availableOperators):
	expression = numberA + operator + numberB
	answer = eval(expression)

	print(answer)
else:
	print("Error")
