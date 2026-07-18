import string

def count_specific_words(): 
    word = input("Word to count: ")
    count = 0
    ## choose file to read and type of encoding 
    with open("harry.txt", "r", encoding="utf-8", errors="ignore") as file: 
        for line in file:
            words = line.split()
            count += words.count(word)
    print(count)

def count_words():
    ## it read a file then splits string(file) into a list of words after every space
    with open("harry.txt", "r", encoding="utf-8", errors="ignore") as file:
        print(len(file.read().split()))

def print_uniwords():
    translator = str.maketrans("", "", string.punctuation + "”" + "’" + "ˇ" + "‘")
    with open("harry.txt", "r", encoding="utf-8", errors="ignore") as file:
        words = [
            word.translate(translator)
            for word in file.read().lower().split()
        ]
        words = [word for word in words if word]
        unique_words = sorted(set(words))
        print(f"Unique words: {(unique_words)}")
print_uniwords()




