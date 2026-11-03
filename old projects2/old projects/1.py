def main():
    while True:
        try:
            i = int(input("Enter a number: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if i <= 0:
            print("Please enter a non-negative number.")
            break
        else:
            while i:
                print("meow")
                i -= 1
main()
        



