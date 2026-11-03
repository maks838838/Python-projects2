
##text = input("write smt ")
##print(text[::-1])

def count_letter(text, letter):
    value=0
    for char in text:
        if letter == char:
            value+=1

    print(value)
##count_letter("hello", "l")
def remove_spaces(text):
    list_of_char = []
    for char in text:
        if char != " ":
            list_of_char.append(char)
    print("".join(list_of_char))
##remove_spaces("hello world")
def largest_number(list_of):
    largest = 0
    for number in list_of:
        if number > largest:
            largest = number
    print(largest)
#largest_number([3, 7, 2, 9, 4]) 
balance = 0 
def main():
    global balance 
    print(balance)
    balance +=100
    print(balance)
    withdraw(10000)
    print(balance)
def withdraw(n):
    global balance
    balance += n

main()