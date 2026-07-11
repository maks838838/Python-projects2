pip install streamlit
streamlit hello
def main():
    print("when is my birthday?")
    day = int(input("what is the number of the day ? "))
    month = int(input("what is the number of the month ? "))
    year = int(input("what is the number of the year ? "))
    correct = 0
    if day == 28:
        correct += 1
    if month == 3:
        correct += 1
    if year == 2003:
        correct += 1
    if correct == 3:
        print("you are correct")
    print("you got", correct, "out of 3 correct")
    if correct < 3:
        main()
main()               

