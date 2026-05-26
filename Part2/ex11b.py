def calculate(num1,operator,num2):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        return num1 / num2
    else:
        return "Invalid operator"
    

print(calculate(10, "+", 5))
print(calculate(10, "-", 5))
print(calculate(10, "*", 5))
print(calculate(10, "/", 5))