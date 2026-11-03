def hello(to="human"):
    print("hello there", to )
hello()
name = input("what is your name? ").title().strip()
hello(name)
age = int(input("what is your age? "))
if age >= 18:
    print("You are an adult.")
elif age < 18:
    print("You are not an adult.")