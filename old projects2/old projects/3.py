def main1():
    y = main()
    print("y is", y)
def main():
    while True:
        try:
            return int(input("Enter a number: "))
        except ValueError:
            pass
main1()