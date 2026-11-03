def main():
    file = open("result.txt", "a")
    for _ in range(5):
        try:
            x = int(input("what is x?"))
        except ValueError:
            continue
        result = square(x)
        print("x squared is", result)
        file.write(f"{result}\n")
    file.close()

def square(n):
    return n * n
main()
