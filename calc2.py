def main():
    file = open("result.txt", "a")
    for _ in range(5):
        x = int(input("what is x?"))
        result = square(x)
        print("x squared is", square(x))
        file.write(f"{result}\n")
    file.close()

def square(n):
    return n * n



main()
