def intro():
    name = input("print your name? ").title().strip() 
    print("Hello", name)
def calc():
    while True:
        act = input("Choose an action (*, /, +, //, **, %, or -): ")
        if act not in ("*", "/", "+", "//", "**", "%", "-"):
            print("Invalid action. Please choose a valid action.")
            continue
        if act in ("**"):
            print("Note: For '**' operations, the second number should be an integer.")
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
        else:
            print("invalid action")
            continue
        print("Result:",x, act, y, "=", result)
        again = input("Do you want to perform another calculation? (y/n): ").lower().strip()
        if again != "y":
            print("Thank you for using the calculator. Goodbye!")
            break        
print("Welcome to the calculator")
calc()

