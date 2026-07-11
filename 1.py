def main():
    while True:
        try:
            i = int(input("Enter a number: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if i < 0:
            print("Please enter a non-negative number.")
            break
        elif i >= 0:
            while i:
                print("meow")
                i -= 1
            
        

def main1():
    while True:
        try:
            i = int(input("Enter a number: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if i < 0:
            print("Please enter a non-negative number.")
        elif i >= 0:
            for i in range(i):
                print("meow")
            
def main2():
    while True:
        try:
            i = int(input("Enter a number: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
    if i > 0:
        for i in range(i):
            print("meow")
        
main1()
        



