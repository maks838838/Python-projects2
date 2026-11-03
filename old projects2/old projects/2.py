
def calc():
    print("Welcome to the calculator")
    while True:
        act = input("Choose an action (*, /, +, //, **, %, or -): ")
        if act not in ("*", "/", "+", "//", "**", "%", "-"):
            print("Invalid action. Please choose a valid action.")
            continue
        try:
            x = float(input("Enter the first number: "))
            y = float(input("Enter the second number: "))
        except ValueError:
            print("Please enter valid numbers.")
            continue
        if y == 0 and act in ("/", "//", "%"):
            print("You cannot divide by zero. Try again.")
            continue
        if act == "*":
            result = x * y
        elif act == "/":
            result = x / y
        elif act == "+":
            result = x + y
        elif act == "-":
            result = x - y
        elif act == "**":
            result = x ** y
        elif act == "//":
            result = x // y
        elif act == "%":
            result = x % y
        print("Result:",x, act, y, "=", result)
        again = input("Do you want to perform another calculation? (y/n): ").lower().strip()
        if again != "y":
            print("Thank you for using the calculator. Goodbye!")
            break        
calc()

