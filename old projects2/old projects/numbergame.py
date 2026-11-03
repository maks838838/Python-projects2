import random
def game():
    while True:
        choice = input("Please select the difficulty level: ").lower()
        if choice == "easy" or choice == "1":
            n = 10
            break
        elif choice == "medium" or choice == "2":
            n = 5
            break
        elif choice == "hard" or choice == "3":
            n = 3
            break
        else:
            print("Wrong, choose 1, 2, 3 or easy, medium, hard")
            continue
    print("Game started, make a guess: ")
    number = random.randint(1, 100)
    won = False
    while n:
        try:
            chance = int(input("pick a number: "))
        except ValueError:
            print("enter a number")
            continue
        if chance < 1 or chance > 100:
            print("choose a number between 1 and 100: ")
            n -= 1 
            continue
        if number == chance:
            print("you won")
            won = True
            print(f"Attempts left: {n-1}")
            break
        elif chance > number:
            print("the number is less than: ", chance)
            print(f"Attempts left: {n-1}") 
        elif chance < number:
            print("the number is greater than: ", chance)
            print(f"Attempts left: {n-1}")
        n -= 1
    if won:
        print("CONGRATS!!!")
    if not won:
        print(f"You lose! The number was {number}.")
    return won
def main():
    difficulty = ["1. Easy (10 chances)", 
    "2. Medium (5 chances)", 
    "3. Hard (3 chances)"]
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    for option in difficulty:
        print(option)
    won = game()
    while True:
        ask = input("want to play again y/n? ").lower()
        if ask == "y":
            won = game()
        else:
            print("goodby looser")
            break
main()

